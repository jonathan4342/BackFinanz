"""Prueba de integración: recorre la API real contra una BD SQLite.

Ejercita el flujo completo (controller -> service -> repository -> BD) para
un cliente y sus tickets, incluyendo los casos de error principales.
"""


def test_full_client_ticket_flow(client_app):
    # 1. Crear un cliente
    resp = client_app.post(
        "/clients",
        json={"name": "Ana", "email": "ana@x.com", "company": "Finanz"},
    )
    assert resp.status_code == 201
    client_id = resp.json()["id"]

    # 2. Email duplicado -> 409
    dup = client_app.post(
        "/clients",
        json={"name": "Otra", "email": "ana@x.com", "company": "Finanz"},
    )
    assert dup.status_code == 409

    # 3. Listar y consultar por id
    assert len(client_app.get("/clients").json()) == 1
    assert client_app.get(f"/clients/{client_id}").status_code == 200
    assert client_app.get("/clients/999").status_code == 404

    # 4. Crear un ticket asociado
    ticket_resp = client_app.post(
        "/tickets",
        json={
            "client_id": client_id,
            "title": "Error de login",
            "description": "No puedo entrar",
        },
    )
    assert ticket_resp.status_code == 201
    ticket = ticket_resp.json()
    assert ticket["status"] == "Pendiente"

    # 5. Ticket con cliente inexistente -> 404
    assert (
        client_app.post(
            "/tickets",
            json={"client_id": 999, "title": "X", "description": "Y"},
        ).status_code
        == 404
    )

    # 6. Actualizar el estado del ticket
    updated = client_app.patch(
        f"/tickets/{ticket['id']}/status", json={"status": "En progreso"}
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "En progreso"

    # 7. Estado inválido -> 422
    assert (
        client_app.patch(
            f"/tickets/{ticket['id']}/status", json={"status": "Cerrado"}
        ).status_code
        == 422
    )

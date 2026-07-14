# Integración con Salesforce

Propuesta técnica para integrar la aplicación de gestión de clientes y tickets con Salesforce, manteniendo PostgreSQL como fuente operativa y Salesforce como CRM.

## Objetos de Salesforce

- **Account** — representa a la **empresa** del cliente (campo `company`).
- **Contact** — representa al **cliente** (nombre, correo), relacionado con su Account.
- **Case** — representa cada **ticket** de soporte. Se mapea el estado a `Status` y se relaciona con el Contact/Account. Es el objeto estándar de Salesforce para soporte, por lo que evitamos crear objetos personalizados.
- Se añade un campo externo `External_Id__c` (External ID, único) en Contact y Case para guardar el `id` de nuestra base de datos y permitir *upserts* idempotentes.

## Información que se sincronizaría

| Nuestra app | Salesforce |
|-------------|-----------|
| Cliente (nombre, correo, empresa) | Contact + Account |
| Ticket (título, descripción) | Case (Subject, Description) |
| Estado del ticket (Pendiente / En progreso / Finalizado) | Case.Status |
| Eventos de auditoría (MongoDB) | Opcional: quedan en nuestro sistema; se pueden reflejar como Case History |

La sincronización sería **bidireccional**: altas de clientes/tickets viajan de la app a Salesforce; los cambios de estado de un Case en Salesforce vuelven a la app. La app expondría un endpoint webhook (`POST /integrations/salesforce/case-updated`) y usaría la **REST API** de Salesforce (con OAuth 2.0, flujo *Client Credentials* o *JWT Bearer* para server-to-server) para escribir hacia Salesforce mediante *upsert* por `External_Id__c`.

## Ejemplo de Apex Trigger

Cuando cambia el estado de un Case en Salesforce, se notifica a la app mediante una llamada asíncrona (`@future callout`):

```apex
trigger CaseStatusSync on Case (after update) {
    List<Id> changed = new List<Id>();
    for (Case c : Trigger.new) {
        Case old = Trigger.oldMap.get(c.Id);
        if (c.Status != old.Status && c.External_Id__c != null) {
            changed.add(c.Id);
        }
    }
    if (!changed.isEmpty()) {
        CaseSyncService.notifyApp(changed); // método @future (callout=true)
    }
}
```

## Ejemplo de componente LWC

Muestra los tickets (Cases) del cliente autenticado dentro de Experience Cloud:

```javascript
// myTickets.js
import { LightningElement, wire } from 'lwc';
import getMyCases from '@salesforce/apex/CaseController.getMyCases';

export default class MyTickets extends LightningElement {
    @wire(getMyCases) cases;
}
```

```html
<!-- myTickets.html -->
<template>
    <lightning-card title="Mis tickets">
        <template for:each={cases.data} for:item="c">
            <p key={c.Id}>{c.Subject} — {c.Status}</p>
        </template>
    </lightning-card>
</template>
```

## Exposición mediante Experience Cloud

Se publica un **sitio de Experience Cloud** (portal de clientes) donde cada cliente inicia sesión con un usuario de comunidad asociado a su Contact. Ahí se embebe el componente LWC `myTickets` para que el cliente vea y siga el estado de sus tickets en autoservicio. El acceso a los datos se controla con perfiles/permission sets y **sharing rules** para que cada usuario solo vea sus propios Cases. Para consumo programático desde la app, Experience Cloud también puede exponer **APIs REST vía Apex REST** (`@RestResource`) protegidas por OAuth.

# Arquitectura de Componentes de UniManage

Este documento describe los componentes principales del sistema UniManage, sus interfaces y las relaciones entre ellos.

## 1. Lista de Componentes

El sistema está compuesto por tres componentes principales:

*   **Frontend:** Es la capa de presentación con la que interactúa el usuario. Está construida con HTML, CSS (utilizando el framework Tailwind CSS) y JavaScript. Las plantillas son renderizadas por el backend de Django.
*   **Backend:** Es el servidor de la aplicación, desarrollado en Python con el framework Django. Se encarga de la lógica de negocio, la autenticación de usuarios, el procesamiento de solicitudes y la comunicación con la base de datos.
*   **Base de Datos:** Es el sistema de almacenamiento persistente de la aplicación. Guarda toda la información de los usuarios, activos, préstamos, eventos, etc. La interacción con la base de datos se gestiona a través del ORM de Django.

## 2. Lista de Interfaces

Las interfaces definen los puntos de comunicación entre los componentes:

*   **API REST (Interna):** Aunque no se expone una API REST pública, el sistema utiliza endpoints internos para la comunicación asíncrona entre el frontend (JavaScript) y el backend. Un ejemplo es la funcionalidad del chatbot, que envía y recibe mensajes sin recargar la página.
*   **Vistas Web (HTML Renderizado):** Es la interfaz principal para los usuarios. El backend de Django renderiza páginas HTML que se muestran en el navegador del usuario.
*   **Conexión SQL (ORM de Django):** Es la interfaz de comunicación entre el backend y la base de datos. Django abstrae las consultas SQL a través de su Mapeo Objeto-Relacional (ORM), permitiendo interactuar con la base de datos utilizando código Python.

## 3. Mapa de Relaciones

El siguiente mapa describe cómo los componentes se conectan a través de las interfaces:

| Componente (Proveedor) | Interfaz | Componente (Consumidor) | Dependencia |
| :--- | :--- | :--- | :--- |
| Backend | Vistas Web | Frontend | El Frontend **depende del** Backend para obtener las páginas HTML. |
| Backend | API REST (Interna) | Frontend | El Frontend **depende del** Backend para funcionalidades dinámicas (ej. chatbot). |
| Backend | Conexión SQL | Base de Datos | El Backend **depende de la** Base de Datos para persistir y recuperar datos. |

### Resumen de Dependencias:

*   El **Frontend** depende del **Backend**.
*   El **Backend** depende de la **Base de Datos**.

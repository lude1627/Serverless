# Serverless
python ft FastAPI

## API de logeo 
La API DE `login` nos permite generar una session vigente para hacer consultas en la base de datos


### Login (POST)
http://localhost:3000/login/sign_in

```json
{
  "username": "Luis",
  "password": "123"
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "Usuario logeado exitosamente"
}
```

## register (POST)
http://localhost:3000/user/register

```json
{
    "User_id": "10",
    "User_name": "Raul",
    "User_phone": "321321",
    "User_mail": "rgmail@.com",
    "User_password": "123ABC.*"
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "Usuario registrado exitosamente"
}
```

## actualizar usuario (PUH)
http://localhost:3000/user/update

```json
{
    "User_id": "10",
    "User_name": "Raul Mendoza",
    "User_phone": "321654",
    "User_mail": "raulgmail@.com",
    "User_password": "123456789.@*"
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "Usuario actualizado exitosamente"
}
```

## ver usuario (GET)
http://localhost:3000/user/view/10

```json
{
    
}
```
### Request Response
```json
{
    "id": 10,
    "username": "Castro",
    "phone": 321321,
    "email": "SrROC@gmail.com",
    "password": "123"
}
```

## crear categoria (POST)
http://localhost:3000/category/create

```json
{
    "id": "3",
    "name": "para toda la familia"

}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "categoria creada exitosamente"
}
```

## ver categorias (GET)
http://localhost:3000/category/view/data

```json
{

}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "Se muestra la lista de categorias en forma de tabla"
}
```

## eliminar categoria (DELETE)
 http://localhost:3000/category/delete/2

```json
{
    
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "categoria eliminada exitosamente"
}
```

## agregar productos (POST)
 http://localhost:3000/product/create

```json
{
    "name": "pizza",
    "description": "todos los sabores, todos los colores y todas las dimenciones",
    "cant": 50,
    "price": 1000,
    "category_id": 123456
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "producto creado exitosamente"
}
```

## ver productos (GET)
http://localhost:3000/category/view/data

```json
{

}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "Se muestra la lista de productos en forma de tabla"
}
```

## actualizar productos (PUH)
http://localhost:3000/product/edit/{id}

```json
{
    "name": "pizza",
    "description": "todos a comer pizza",
    "category_id": 123456,
    "cant": 55,
    "price": 1500
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "producto actualizado exitosamente"
}
```

## eliminar productos (DELETE)
http://localhost:3000/product/delete/{id}

```json
{
    
}
```
### Request Response
```json
{
  "statusCode": "200",
  "message": "producto eliminado exitosamente"
}
```

# Marple Datatypes API

- `/datatype`: List all available datatypes

```json
[
    {
        "id": "swedish_municipalities",
        "label": "Swedish municipalities",
        "path": "http://marple-datatypes.herokuapp.com/datatype/swedish_municipalities"
    }
]
```

- `/datatype/{DATATYPE}`: Get allowed values for a specific datatype

```json
{
    "id": "swedish_municipalities",
    "allowed_values": [
        {
            "id": "Stockholms kommun",
            "path": "http://marple-datatypes.herokuapp.com/item/Stockholms kommun"
        }
    ]
}
```

- `/item/{ITEM_ID}`

```json
{
    "id": "Stockholms kommun",
    "label": "Stockholms kommun",
    "parent": {
        "id": "Stockholms län",
        "label": "Stockholms län",
        "path": "http://marple-datatypes.herokuapp.com/item/Stockholms län"
    },
    "children": [
        {
            "id": "Södermalm stadsdelsområde",
            "label": "Södermalm stadsdelsområde",
            "path": "http://marple-datatypes.herokuapp.com/item/Södermalm stadsdelsområde"
        }
    ],
    "neighbours": [
        {
            "id": "Solna kommun",
            "label": "Solna kommun"
            "path": "http://marple-datatypes.herokuapp.com/item/Solna kommun"
        }
    ]
}
```

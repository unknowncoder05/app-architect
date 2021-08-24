# App architect

```sh
python .\compiler\compiler.py c "django.json.v1" ./blueprints/examples/facebook/main.app.json ./compiler/build
```
Design your application in a json like structure, this way the resulting project is going to be easily understood both by human and by machine.

This json like structure will let you:
- Design your application in a visual application, speeding up and formalizing the process (visual software is still under development)
- Compile to any language (compilers are still under development)
- Manipulate your app using simple code

## Compilers
A Compiler takes a well defined json like project and translates it to a specyfic language or framework, generating a functional and readable code ready to be executed and easy to edit
## Syntax Documentation

### App component
Denoted with the extension ".app.json" (ex: "main.app.json")

this file is in charge of calling all required models and services

### Model component
Denoted with the extension ".model.json" (ex: "user.model.json")

defines all the models for a specific entity and its different variants depending the use case

### Service component
Denoted with the extension ".service.json" (ex: "auth.service.json")

defines the inputs, input processing and outputs of a certain request

## Global special attributes

### __constructor
lets you specify wich attributes can be modified and are required

use case:

``` js
// basic_math_service.service.json
{
    "__constructor":{
        "number_a" : {
            "description": "first number to be operated"
            "default": 1
        },
        "number_a" : {
            "description": "second number to be operated"
            "default": 2
        }
    },
    "endpoints":{
        "sum numbers":{
            "request":{
                "__number_a" : {
                    "type": "int",
                },
                "__number_b" : {
                    "type": "int",
                }
            },
            "response":{
                "answer" : {"type": "int"}
            }
        },
    }
}
```

now you can call it like
``` js
//main.app.json
{
    "services":{
        "math": {
            "__from":"basic_math_service.service.json"
            "number_a":3,
            "number_b":4,
        }
    }
}
```
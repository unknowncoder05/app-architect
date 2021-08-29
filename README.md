# App architect

### Python Compiler
There is no faster way for understanding than trying it yourself.
you can execute the next command in the root of the project (this folder) and a simple code wil be generated.
```sh
python .\compiler\compiler.py c "python.json.v1" ./blueprints/examples/calculator/v2/services/processing/operations/sum.code.json code.py
```

You can check the base blueprint for this project in the route examples/calculator/v2/services/processing/operations/sum.code.json

```py
def sum(number_a:int, number_b:int, *, debug:bool=False)->int:
        result:str = number_a+number_b
        if debug:
                print(result)
        return result
```
This is the expected answer, a simple function with all that we specified in the code.json file and ready to be used.

#### What is so special about this?
This is a basic format for you to generate code in any language, in any framework as long as the correct compiler is available.

### Current roadmap for this project

- Finish the basic Python compiler
- Add tests
- Work in the JS Express compiler
- Create a UI from where to Edit code and generate the proper code.json, then you can choose from your saved snippets or those that other people had made public
### App Compiler
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
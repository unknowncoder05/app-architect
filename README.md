# App architect

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
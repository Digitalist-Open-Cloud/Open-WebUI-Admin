# Example debugging

## Custom model not working

You have setup a model called "Office help" which is using another model, let us say XGPT-45.

Suddenly it stops working and says "Model not found". You go into to edit the model to see what
is going on. You know see that the base model is gone. That could be of many resasons like the model
stopped to exist, have been removed, have new version instead etc.

In Open WebUI there is not way to see which model you used before.

Using the cli you can get that information:

List all models and what base model they are using:

```shell
open-webui-admin models custom list
```

```shell
ID                                     BASE
-------------------------------------  ------------------------------------
office-help                            xgpt-45
carbon-copy                            chatgpt-4o-latest
```


Or a verbose listing with all the information about that specific model you set up:

```shell
open-webui-admin models custom list --name office-help
```

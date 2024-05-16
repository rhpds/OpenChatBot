def read_config_file(config_file):
    print("DEBUG: read_config_file(config_file):",config_file)
    import yaml
    with open(config_file, 'r') as file:
        config_vars = yaml.safe_load(file)
    return config_vars


async def setup_chat_settings(chat_settings_defaults):
    import chainlit as cl
    from chainlit.input_widget import Select, Switch, Slider
    print("DEBUG: setup_chat_settings(chat_settings_defaults):",chat_settings_defaults)


    widgets = []
    print(chat_settings_defaults)
    for widget_data in chat_settings_defaults:
        if widget_data['type'] == 'select':
            widget = Select(**widget_data)
        elif widget_data['type'] == 'switch':
            widget = Switch(**widget_data)
        elif widget_data['type'] == 'slider':
            widget = Slider(**widget_data)
        widgets.append(widget)
    
    #print("widgets: \n ", widgets)
    
    settings = await cl.ChatSettings(widgets).send()
    
    return settings

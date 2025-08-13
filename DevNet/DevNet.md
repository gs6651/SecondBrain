
Data Formats:
 - JSON
 - XML
 - YAML
```
    import yaml
    with open("yaml_example.yml", 'r') as file:
        data = yaml.safe_load(file)                         ! Converting a YAML file to a Python dictionary
    user = data['user]
    print(user['name'])
    for role in user['roles']:
    print(role)



    user['location']['city'] = 'Dallas'
    with open('yaml_example-edited.yml', 'w') as file:
        yaml.dump(data, file, default_flow_style = False)   ! From a Python dictionary, saving to a YAML file
```


APIs considerations:
 - Modular software design
 - Prototyping and testing API integration
 - Challenges in consuming networked APIs
 - Distributed computing patterns



## parent 
### send a data in a serialized format json
from django.core.serializers import serialize

parent_data = serialize('json', [object.parent])

### sending
'parent': parent_data,


## opened till a level
def generate_tree_data():
    data = []
    for node in your_nodes:  # Assuming you iterate over your nodes
        level = node.level  # Assuming nodes have a level attribute
        is_opened = level < 3  # Open up to level 2 (0-indexed)
        data.append({
            'id': node.id,
            'parent': node.parent_id or '#',
            'text': node.text,
            'state': {'opened': is_opened}
        })
    return json.dumps(data)
### html 
$('#your-tree').jstree({
  'core' : {
    'data' : JSON.parse(your_json_data_from_server)
  }
});



### this is the sample JSTREE SUBMENU
"MoreOptions": {
          "label": "More Options",
          "submenu": {
            "Option1": {
              "label": "Option 1",
              "action": function(obj) {
                // Your option 1 action here
              },
            },
            "Option2": {
              "label": "Option 2",
              "action": function(obj) {
                // Your option 2 action here
              },
            },
            "Submenu": {
              "label": "Another Submenu",
              "submenu": {
                "SubOption1": {
                  "label": "Sub-Option 1",
                  "action": function(obj) {
                    // Your sub-option 1 action here
                  },
                },
                "SubOption2": {
                  "label": "Sub-Option 2",
                  "action": function(obj) {
                    // Your sub-option 2 action here
                  },
                }
              }
            }
          }
        },
You can use jQuery's `$.ajax()` method to fetch the HTML content of the new page (template) and insert it into the `details_div`.

Here's an example of how you could go about this:

1. **Django View**: First, create a Django view to render the template to an HTML string.

    ```python
    from django.shortcuts import render
    from django.http import HttpResponse
    
    def fetch_template(request):
        # Logic to fetch necessary data, if needed
        return render(request, "your_template.html")
    ```

2. **URLs**: Map the new view to a URL.

    ```python
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path('fetch_template/', views.fetch_template, name='fetch_template'),
        # other urls
    ]
    ``` 

3. **Ajax call in jsTree**: Make an Ajax call to the new URL when a node is selected.

    ```javascript
    $('#jstree').on("select_node.jstree", function (e, data) {
        const nodeId = data.node.id;
        $.ajax({
            url: '/fetch_template/',
            method: 'GET',
            data: { 'nodeId': nodeId },  // Pass node ID or other info to the server if needed
            success: function (response) {
                // Insert the fetched HTML into details_div
                $('#detailsDiv').html(response);
            },
            error: function (error) {
                console.log('Error fetching template:', error);
            }
        });
    });
    ```

This will fetch the new template from the server when a node is clicked, and insert it into the `detailsDiv`.

Just replace `"your_template.html"` with the name of the template you wish to load. You can also add more logic in the `fetch_template` Django view to fetch specific data based on the `nodeId`, which can be passed as a query parameter in the Ajax request.

Is this approach suitable for your project?
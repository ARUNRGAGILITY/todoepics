# common variables

# project urls
project_urls = """

"""

# urls
urls = """

"""

# View
view_code = """
# add ovs 
@login_required(login_url='login')
def add_ovs(request):
    if request.method == 'POST':
        form = OpsValueStreamForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            vsm = form.save()            
            return redirect('ops_valuestream_mgmt')
    else:
        form = OpsValueStreamForm()
    
    context = {'page': 'add_ovs', 'form': form}
    template_file = f"{app_name}/_3admin/valuestream_mgmt/add_ops_valuestream.html"
    return render(request, template_file, context)
    
# delete ovs
@login_required(login_url='login')
def delete_ovs(request, id):
    object = get_object_or_404(OpsValueStream, id=id)
    context = {'object': object}
    if request.method == 'POST':
        OpsValueStream.objects.filter(id=id).update(active=False, deleted=False,  author=request.user)
        return redirect('ops_valuestream_mgmt')
    template_file = f"{app_name}/_3admin/valuestream_mgmt/delete_ops_valuestream.html"
    return render(request, template_file, context)
"""

# template
template_code = """

"""



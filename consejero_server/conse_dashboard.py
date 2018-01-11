from admin_tools_stats.modules import DashboardCharts, get_active_graph
from admin_tools.dashboard import Dashboard,modules

class ConseDashboard(Dashboard):
	# append an app list module for "Country_prefix"
	self.children.append(modules.AppList(
	    _('Dashboard Stats Settings'),
	    models=('admin_tools_stats.*', ),
	))

	# Copy following code into your custom dashboard
	# append following code after recent actions module or
	# a link list module for "quick links"
	graph_list = get_active_graph()
	for i in graph_list:
	    kwargs = {}
	    #kwargs['chart_size'] = "260x100" # uncomment this option to fix your graph size
	    kwargs['graph_key'] = i.graph_key
	    if request.POST.get('select_box_'+i.graph_key):
	        kwargs['select_box_'+i.graph_key] = request.POST['select_box_'+i.graph_key]


	    self.children.append(DashboardCharts(**kwargs))	
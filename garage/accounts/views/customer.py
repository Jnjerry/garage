from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from ..suggestions import update_clusters
from ..decorators import customer_required
from ..forms import CustomerSignUpForm,ReviewForm
from ..models import User, Vehicle,Cluster, MechProfile, Review,Repair
from django.db import models
from django.http import HttpResponse

from ..filters import  VehicleFilter
import datetime

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request,"Successfully signed up")
        return redirect('login')

@method_decorator([login_required,customer_required], name='dispatch')
class VehicleDetailView(DetailView):
    model = Vehicle
    context_object_name = 'vehicle'
    template_name = 'accounts/customer/vehicle_detail.html'

@method_decorator([login_required,customer_required], name='dispatch')
class VehicleListView(ListView):
    model = Vehicle
    paginate_by = 3
    ordering = ('licenceplate',)
    context_object_name = 'vehicles'
    template_name = 'accounts/customer/vehicle_list.html'


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['vehicles']=VehicleFilter(self.request.GET,queryset=self.get_queryset())
        return context



    def get_queryset(self):
        queryset = self.request.user.owner\
        .select_related('name')
        return queryset




@method_decorator([login_required,customer_required], name='dispatch')
class VehicleCreateView(CreateView):
    model =  Vehicle
    context_object_name = 'vehicle'
    fields = ('vehicle_name','type','car_model','number_plate','image','ownership','status','image1','image2')
    template_name = 'accounts/customer/vehicle_add_form.html'


    def form_valid(self, form):
        vehicle=form.save(commit=False)
        vehicle.name=self.request.user
        vehicle.save()
        messages.success(self.request,"Vehicle updated with success")
        return redirect('customer:vehicle_list')

#
# def custdashboard(request):
#         items = Vehicle.objects.all()
#         return render(request,'accounts/reports/custdashboard_list.html',context={'items':items})
@login_required()
def homepage(request):
        items = Vehicle.objects.all()
        return render(request,'accounts/home.html',context={'items':items})



@method_decorator([login_required,customer_required],name='dispatch')
class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ('vehicle_name','type','make','car_model','number_plate','image','ownership','status')
    context_object_name = 'vehicles'
    template_name = 'accounts/customer/vehicle_change_form.html'

    def form_valid(self, form):
        vehicle=form.save(commit=False)
        vehicle.name=self.request.user
        vehicle.save()
        messages.success(self.request,"Vehicle updated with success")
        return redirect('customer:vehicle_change', vehicle.pk)

    def get_success_url(self):
        return reverse('customer:vehicle_change',kwargs={'pk':self.object.pk})


@method_decorator([login_required, customer_required], name='dispatch')
class VehicleDeleteView(DeleteView):
    model = Vehicle
    context_object_name = 'vehicle'
    template_name = 'accounts/customer/vehicle_delete_form.html'
    success_url = reverse_lazy('customer:vehicle_list')

    def delete(self, request, *args, **kwargs):
        vehicle= self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.owner





def add_review(request, mechprofile_id):
    mechprofile = get_object_or_404(MechProfile, pk=mechprofile_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.mechprofile = mechprofile
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('customer:profile_detail', args=(mechprofile.id,)))

    return render(request, 'accounts/mechanic/profile_detail.html', {'mechprofile': mechprofile, 'form': form})

#initially a user can request for a mechanic even before they have used the site before
#essentially we eant to return mechanics not reviewed by the user
@login_required
def user_recommendation_list(request):
    #get user reviewed mech
    #we get a list of mech ids requested by the user
    user_reviews=Review.objects.filter(user_name=request.user.username).prefetch_related('mechprofile')
    user_reviews_mechprofile_ids=set(map(lambda x: x.mechprofile.id, user_reviews))


    # get request user cluster name (just the first one right now)
    # so here just want to get the cluster name the request user belongs to
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except: # if no cluster assigned for a user, update clusters
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    #get usernames for other members of the cluster
    #exlude the request user just to reduce query time
    user_cluster_other_members =\
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # get reviews by those users(in the cluster),excluding  reviewed by the request user
    other_users_reviews =\
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(mechprofile__id__in=user_reviews_mechprofile_ids)
    other_users_reviews_mechprofile_ids= set(map(lambda x: x.mechprofile.id, other_users_reviews))

    #then get a mechanic list including the previous IDS,order by rating


    mech_list=sorted(
        list(MechProfile.objects.filter(id__in=other_users_reviews_mechprofile_ids)),
        key=lambda  x: x.average_rating(),
        reverse=True
    )

    return render(
        request,
        'accounts/customer/user_recommendation_list.html',
        {'username': request.user.username,'mech_list': mech_list}
    )

@method_decorator([login_required,customer_required], name='dispatch')
class MechListView(ListView):
    model = MechProfile
    # ordering = ('user_name', )
    context_object_name = 'mechprofile'
    template_name = 'accounts/customer/mech_list.html'




def VehicleExport(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response



@method_decorator([login_required,customer_required], name='dispatch')
class VehicleRepairCreateView(CreateView):
    model = Repair
    context_object_name = 'repair'
    fields = ('vehicle','summary','description','mileage','priority','image')
    template_name = 'accounts/customer/repair_add_form.html'



    def form_valid(self, form):
        repair=form.save(commit=False)
        repair.name=self.request.user
        repair.save()
        messages.success(self.request,'Issue created successfully')
        return redirect('customer:repair_list')

@method_decorator([login_required,customer_required], name='dispatch')
class VehicleRepairListView(ListView):
        model = Repair
        context_object_name = 'repair'
        template_name = 'accounts/customer/repair_list.html'


        # def get_queryset(self):
        #     repair = Repair.objects.filter(user=self.request.user)
        #     return repair


@method_decorator([login_required,customer_required], name='dispatch')
class VehicleUpdateView(UpdateView):
    model = Repair
    context_object_name = 'repair'
    fields = ('vehicle','summary','description','mileage','priority','image')
    template_name = 'accounts/customer/repair_change_form.html'



    def form_valid(self,form):
        repair=form.save(commit=False)
        repair.name=self.request.user
        repair.save()
        messages.success(self.request,'Issue updated successfully')
        return redirect('customer:repair_change',repair.pk)

    def get_success_url(self):
        return reverse('customer:repair_change',kwargs={'pk':self.object.pk})



@method_decorator([login_required,customer_required], name='dispatch')
class VehicleDeleteView(DeleteView):
    model = Repair
    context_object_name = 'repair'
    template_name = 'accounts/customer/repair_delete_form.html'
    # success_url = reverse_lazy('customer:repair_delete')

    def delete(self, request, *args, **kwargs):
        repair = self.get_object()
        messages.success(request, ' repair was deleted with success!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('customer:repair_list')


@method_decorator([login_required,customer_required], name='dispatch')
class VehicleRepairDetailView(DetailView):
    model = Repair
    context_object_name = 'repair'
    template_name = 'accounts/customer/repair_detail.html'

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    mech = MechProfile.objects.all()
    context = {'latest_review_list':latest_review_list, 'username':username , 'mech':mech}
    return render(request, 'accounts/ratings/user_review_list.html', context)

#
def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'accounts/ratings/review_list.html', context)








#
# def user_review_list(request, username=None):
#     if not username:
#         username = request.user.username
#     latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
#     context = {'latest_review_list':latest_review_list, 'username':username}
#     return render(request, 'reviews/user_review_list.html', context)



# def mech_list(request):
#     mech_list = MechProfile.objects.order_by('-name')\
#       .values('name') \
#         # .annotate(average_rating=Count('name', filter=Q(survived=True)),
#         #           not_verage_rating=Count('name', filter=Q(survived=False))) \
#
#     context = {'mech_list':mech_list}
#     return render(request, 'accounts/customer/mech_list.html', context)

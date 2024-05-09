from datetime import date

# We want to make the shift data available to all templates
def shift_data(request):
    shift = None
    if request.user.is_authenticated:
        shift = request.user.shifts.filter(date=date.today()).first()
    return {'today_shift': shift}

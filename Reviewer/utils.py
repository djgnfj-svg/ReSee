

def form_is_valid(form, _msg):
	if form.is_valid():
		email = form.cleaned_data.get("email")
		raw_password = form.cleaned_data.get("password")
		msg = _msg
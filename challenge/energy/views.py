from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from challenge.energy.exceptions import UploadError
from challenge.energy.forms import UploadFileForm
from challenge.energy.handlers import UploadCSVHandler


@login_required
@require_POST
def upload_csv(request: HttpRequest) -> HttpResponse:
    form = UploadFileForm(request.POST, request.FILES)

    if form.is_valid():
        csv_file = request.FILES["file"]

        try:
            UploadCSVHandler(csv_file, request.user)()

            return redirect("upload_success")
        except UploadError as e:
            form.add_error("file", e.message)

    return render(request, "energy/upload_csv.html", {"form": form})


def upload_success(request: HttpRequest) -> HttpResponse:
    return render(request, "energy/upload_success.html")

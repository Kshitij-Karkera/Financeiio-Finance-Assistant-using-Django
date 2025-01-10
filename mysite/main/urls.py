from django.urls import path

from . import views
urlpatterns = [
   path("", views.Home, name = "Homes"), 
   path("home/", views.Home, name = "Homes"), 
   path("sign/", views.sign_up_in, name = "sign_up_in"),
   path("suggestions/", views.suggestions, name = "suggestions"),
   path("port/", views.portfolio, name="portfolio"),
   path("fpass/", views.forgetpass, name="fp"),
   path("base/", views.base, name="base"),
   path("news/", views.news, name="news"),
   path("setting/", views.settings, name="settings"),
   path("learn/", views.learn, name="learn"),
   path("base2/", views.base2, name="base2"),
   path("blogStk1/", views.blogStk1, name = "blogStk1"),
   path("blogStk2/", views.blogStk2, name = "blogStk2"),
   path("blogStk3/", views.blogStk3, name = "blogStk3"),
   path("blogStk4/", views.blogStk4, name = "blogStk4"),
   path("blogStk5/", views.blogStk5, name = "blogStk5"),
   path("blogStk6/", views.blogStk6, name = "blogStk6"),
   path("blogStk7/", views.blogStk7, name = "blogStk7"),
   path("blogCryp1/", views.blogCryp1, name = "blogCryp1"),
   path("blogCryp2/", views.blogCryp2, name = "blogCryp2"),
   path("blogCryp3/", views.blogCryp3, name = "blogCryp3"),
   path("blogCryp4/", views.blogCryp4, name = "blogCryp4"),
   path("blogCryp5/", views.blogCryp5, name = "blogCryp5"),
   path("blogCryp6/", views.blogCryp6, name = "blogCryp6"),
   path("blogCryp7/", views.blogCryp7, name = "blogCryp7")
]
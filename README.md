# ِDjango Blog

> A Blog developed using Django framework along with a fully customized Management Panel

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
![](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

## Screenshots

![Screenshots of the project](screenshots/index.png)

![Screenshots of the project](screenshots/recent_articles.png)

![Screenshots of the project](screenshots/article_comments.png)

![Screenshots of the project](screenshots/articles.png)

![Screenshots of the project](screenshots/login.png)

![Screenshots of the project](screenshots/admin_panel.png)

# Features

A little about DjangoBlog:

* Used view counter to determine popular articles
* Customized admin panel for superusers
* Fully functional management panel with [AdminLte3](https://adminlte.io/) for SuperUsers, Staff, Authors and regular
  users
* Special articles and subscription
* Signup with E-mail confirmation
* Reset password with E-mail
* Authentication with Google
* Easy share on social media(Twitter, Telegram, Whats app)
* Search bar
* Comment system
* Authorized access to privileged sections

## View Counter

---
Let's say you want to read an article on DjangoBlog. The second you open the article a middleware saves your IP address
and count it as a view for that article. Stored ip addresses are accessible from django's admin panel.

## Management Panel

---
This panels template is from [Adminlte3](https://adminlte.io/), also
with [django crispy forms](https://django-crispy-forms.readthedocs.io/en/latest/#), all forms are supported by
bootstrap4.

![articles_list](screenshots/articles.png)
*Articles list*

![articles_list](screenshots/new_article.png)
*New article*

![comments_list](screenshots/comments.png)
*Comments list*

![comments_list](screenshots/profile.png)
*User Profile*

![comments_list](screenshots/change-password.png)
*Change Password*

## Privileges

---

Privileges and Restricted access are very important matters, so I took them seriously. If someone wants to bypass the
restrictions, will get 404 error or redirects to main page.

On the blog, sending comment and access to special articles requires login. On management panel privileges are a little
more complicated and is as follows:

If you are an active regular or special user you only can access your own profile and change only your Firstname,
Lastname, email and password.

If you are designated as author(author status can set from admin panel by superuser) in addition of futures above:

- Articles: you can add, change, delete(with double confirmation), see preview. Also, as an author you only can submit
  your article for review, and you can't put it on blog directly; your article will be reviewed by staff or superusers.


- comments: you can read and set status(accept or deny) your own articles comments in this case if you deny a comment it
  will delete automatically.

If you are staff (staff status can set from admin panel by superusers) in addition of futures above you have full access
to:

- Articles: add, full modify, delete, set status(accept or deny)


- Comments: see comments and replies in tree view, delete, set status(accept or deny)
  in this case if you deny a comment it will delete automatically.

If you are a superuser... well naturally you can do what the hell you want here and ofcourse from admin panel.

## Special membership

---

Every user has a subscription date, after that date user's special membership will expire and reading special articles
requires special membership without it, user will see only the first 50 words of the text.

![subscription](screenshots/subscription.png)
*subscription*

![subscription expired](screenshots/subscription(2).png)
*subscription expired*

![subscription expired](screenshots/subscription(3).png)
*see more*

## Author

I'm Alireza a CE student and Back-end developer with special interest in Django framework and Django Rest-ful APIs.

Alireza Abavi – abavi.alireza2002@gmail.com

You can find me here at:
[Github](https://github.com/AlirezaAbavi),
[LinkedIn](https://www.linkedin.com/in/alireza-abavi/)

## Credits

A heartfelt thank you to [@mehran-tarif](https://github.com/mehran-tarif) for his awsome tutorials
on [Silicium](https://www.youtube.com/c/Silicium7) !

Thank you to the following awesome geeks for their templates and packages ❤️

* Blog Template: [templatemo](https://templatemo.com/)
* Management Panel Template: [Adminlte3](https://adminlte.io/)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

MIT © AlirezaAbavi
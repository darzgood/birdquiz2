OVERVIEW: 
version 1.1
This program is an online bird quiz intended to help birders sharpen their bird
identification skills. It was built on a shared hosting site on Hostgator using
the micro-framework Flask and a cgi server. 
Versions are recorded as such: x.y
x: major changes in program such as a change in setup or server type
y: minor changes in progam and major bug fixes

CHANGELOG:
v1.3
5-11-18:
1. Edited the z-index of the navigation bar so that it would stay to the front.
2. Added a Resources page
5-31-18:
3. Added new classes to the form_background divs to change the padding between .narrow and .full.
4. Changed z-index of the footer and navigation bar so that the footer stays on top.
5. Added info to the Resources and About pages and edited the CSS stylesheet for them:
8-16-18:
6. Edited database to include "messages" category
7. Added db_README to document database modification. 
8-17-18:
8. Moved quiz messages onto the form background by using the "messages" database category instead 
of flashing the messages to base.html.
9. Added a filter to keep "bird" from being a legitimate guess answer.
10. Added a link to the bird name on final.html
11-?-18:
11. Added photos from tgreybirds.com to photo dir.
12. Changed image storing sytem from using one folder to folders for each photographer.
v1.2
1.Fixed known bug in which the same image can appear twice in the same quiz.
Spring 2018:
2. Added repeating image to background with partial transparency by adding a 
body:after element in the css styesheet.
3. Edited the submit button on the setup page to disable once clicked:
setup.html
4. Added a interactive navigation bar.
5. Added Contact and About pages to the website.
6. Performed many color and style upgrades to the templates.
5-10-18:
7. Replaced <style> attribute in each template with a single css stylesheet in 
the static folder
8. Moved the background image to the static folder.
v1.1
1.The HTML templates were modified to work on multiple browsers instead of 
solely Chrome. Images are now sized using vmin units instead of max-content 
frames.
2.Various other minor edits were made to the HTML templates.
3.A validator was added to name/nickname form on setup to disallow names over 
twenty-five characters in length.

TODO:
1.Replace CGI server with FCGI or WSGI.
2.Add multiple choice options.
3.Add new quiz images.

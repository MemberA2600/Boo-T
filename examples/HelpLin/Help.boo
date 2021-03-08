deliminator hullahopp
basics(author=Fehér János Zoltán (Member),
       language=en, 
       charset=utf-8,
       palette=27) hullahopp

keywords(Help, Boo-T, Bootstrap) hullahopp
description(This is the help file for the Boo-T application) hullahopp
title(Help) hullahopp

background(image=/home/member/PycharmProjects/Boo-T/Back.jpg) hullahopp
font-family("Myriad Pro Light", "Informal Roman", "Gabriola", "Arial") hullahopp
opacity(navbar=0.55, container=0.75, table=0.75, footer=0.55) hullahopp

banner(size=cover, height=450, animation(50s, 
	/home/member/PycharmProjects/Boo-T/Spooky1.jpg,
	/home/member/PycharmProjects/Boo-T/Spooky2.jpg,
	/home/member/PycharmProjects/Boo-T/Spooky3.jpg,	
	/home/member/PycharmProjects/Boo-T/Spooky4.jpg),
	text("Help with Boo-Ting!", 4em, center)
) hullahopp

navbar(brand(image=/home/member/PycharmProjects/Boo-T/ghost.png), expand=xl,
	item("Welcome", welcome),
	item("Basics", basics),
	item("Page Settings", page),
	item("Banner", banner),
	item("NavBar", nav),
	item("BootRow", bootr),
	item("Tables", tables),
	item("Footer", footer)
) hullahopp

bootrow(id=welcome, rate(auto), article(title="Greetings!", title-align=left, rawtext="You just opened the help file for Boo-T and as you can see, it was created in Boo-T as well. Well, well, let's get started!<br>The software was designed to be as simple as it can be for a beginner, so you won't gave up too early! Let me explain the most basic things!<br>In the main windows, you can see the <b>Syntax List</b>, these are the only things you need to work with!<br><br>The software generates an HTML file and <b>injects the CSS</b> into it, the only thing you will find in your folder is the <i>'img'</i> that contains the images you used. Because I don't want you to lose your images, Boo-T <b>will copy them</b> to that folder and changes the path in the HTML file if you are using an absolute path like <i>'C:/Documents/powerpuffgirls.png'</i>.<br>")
) hullahopp

bootrow(id=basics, rate(auto), 
	article(title="I. Basics", 
	title-align=left, 
	rawtext="In the syntax of Boo-T, there are <b>commands</b> and <b>arguments</b>. Commands are the most important, they are at the beginning of lines, they are followed by rounded brackets. The line is always ended by a deliminator, which also separates code and comments, you can write anything after the deliminator till the next newline. So the syntax basically looks like this:<br><br><b><u>command</u></b>(<i>arguments</i>) <i>deliminator</i> comment<br><br>Setting the <b>deliminator</b> is really special compared to the other commands. You can set it only in the very first line of your code (other ones will be ignored), writing '<b><u>deliminator</u></b>' without the rounded brackets you would usually use with commands and putting the desired deliminator <b>after a single space.</b><br>Most commands are only needed to be used once (except for bootrows and tables), the newer ones are just overriding the older ones.<br><b>Arguments</b> are seperated by commas inside the rounded brackets. There are three kind of appearances of arguments:<br><ul><li>Just a single word</il><li>Two words splitted by an equality symbol, like <i>arg=something</i></li><li>A word with rounded brackets, like commands, containing several words seperared by commas, like <i>arg(something,something,something)</i></li></ul>Because of this wrapping you can place spaces and newlines nearly anywhere, so your code can be really easy to read, like I did with the banner for this site:<br><br><u>banner</u>(size=cover, height=450, animation(50s,<br><space:10>E:/PyCharm/P/Boo-T/Spooky1.jpg,<br><space:10>E:/PyCharm/P/Boo-T/Spooky2.jpg,<br><space:10>E:/PyCharm/P/Boo-T/Spooky3.jpg,<br><space:10>E:/PyCharm/P/Boo-T/Spooky4.jpg),<br><space:10>text('Help with Boo-Ting!', 4em, center)<br>) %%<br><br>Now you know the most basic things, we are gonna go for the 'page settings'!")) hullahopp

bootrow(id=page, rate(auto),  
	article(title="II. Page Settings", 
	title-align=left, 
	rawtext="Creating the HTML template for your website can be really boring, so I'm taking care of that for you! These are the things you can set in Boo-T:<ul><li><u>basics</u>(author=,language=,charset=,palette=)<br>Author, language and charset basically just <b>sets the meta tags</b>, if you ignore or forget them, language will be set to <i>english</i> and charset to <i>UTF-8</i> (anything else for charset is <u>not recommanded</u>!) Palette has a basic set of palettes, containing 4 colors for building up the entire site. You can call them by name (you can find them in folder <i>'default/Colors'</i>), use a number between 0-27 or set it to random that will save your site with a random palette each time you save you generate your code.</li><li><u>keywords</u>()<br>You can put there keywords, separated by commas, it will be directly copied to the meta tag on your site.</li><li><u>description</u>()<br>Same as the keywords, it will be copied directly.</li><li><u>title</u>()<br>And this one as well!</li><li><u>background</u>({color, gradient=, image=})<br>Setting the background is really simplified. You can set it to 'color' that will create a solid color. Gradient will produce a color gradient based on the color palette, you can set it to HOR, VER or DIG, representing the direction. If you set it to 'image', de background will be filled with a fixed image.</li><li><u>font-family</u>()<br>This will set the fonts your website gonna use. If you don't set it, Arial will be choosen.</li><li><u>opacity</u>({container=, tables=, navbar=, footer=})<br>Sets opacity for the given elements, default is 1.0. You have to use float numbers between 0.0 and 1.0! </li></ul>"
)) hullahopp

bootrow(id=banner, rate(auto), 
	article(title="III. Banner", 
	title-align=left, 
	rawtext="Banner is a really important part for a website. On small devices, like phones, the banner won't be displayed along with the part outside the container. Inside the <b>banner()</b> command, there are a lot to set. <b>Size</b> can be <i>'contain'</i> or <i>'cover'</i>, left out will display a cover-style banner. <b>Height<b> is the vertical size of your banner in pixels (you <u>don't have</u> to put there 'px'!). The title of your site can be set via the <b>text()</b> argument, it contains three elements, you <u>cannot</u> change their orders!<ol><li><b>"The Title Text as a String"</b></li><li><b>The size of the title text</b>, can be px or em.</li><li><b>The alignment of the text</b>, can be left, center or right</li></ol>There are two ways to set the background picture of the banner:<ul><li><b>image=</b><br>Works as the image argument for the background, it will cover the division.</li><li><b>animation()</b></li>Contains the time and the images, separated by commas. <u>First</u> you have set the time for the whole animation circle, then add the link for the pictures, one by one, creating a list. It will have a blurry, grayscale animation for transition.</li></ul>For the banner example, you can see one at the Basics section!"
)) hullahopp

bootrow(id=nav, rate(auto),  
	article(title="IV. NavBar", 
	title-align=left, 
	rawtext="Navbars are the only navigation tool and you can only add link to ids available on the current site, because on mobile phone, it's a lot easier to use a onepage site with vertical scrolling. Building Navbars is pretty easy, you set if witrh the <b>navbar()</b> command. There are two kind of elements you can add:<ul><li><b>brand({"String", image=})</b><br>Brand is the very item of the navbar which is not affected by the toggle button. The brand can be a <b>"String"</b>, a plaint text or you can add an image tag and put there an image.</li><li><b>item("String", id)<br>Items are the links for the parts of your website. They can be only string items and you have to put there an id that was added to a bootrow, table or footer item.</li><li><b>sticky</b><br>If you set it, the NavBar will stay at the top as you progress scrolling down.</li><li><b>expand=</b><br>You can add here the screen size where the navbar should be expanded. You can use sm, md, lg, xl or a number between 0-4.</li></ul> An example for the NavBar code:<br><u>navbar</u>(brand(image=ghost.png),sticky,expand=xl<br><space:20>item("Item1", item1),<br><space:20>item("Item2", item2),<br><space:20>item("Item3", item3)) %%"
)) hullahopp

bootrow(id=bootr, rate(auto),  
	article(title="V. BootRow", 
	title-align=left, 
	rawtext="BootRows are maybe the most importrant and complex components of your website, you can have more than one, they use the column alignment of Bootstrap. You insert them with the <u>bootrow()</u> command. There are several elements you can add to bootrows:<ul><li><b>id=</b><br>With the id, you can add your row to one of the navbar links. You just have to type it, no string format needed.</li><li><b>rate</b>()<br>Rates can have two kind of values, auto and a list of numbers, separated by commas. If you set it to auto, all the items you will have to fit in the row with the same width. The is great for an image gallery, take this example:</li></ul>"
)) hullahopp

bootrow(rate(auto), 
	image=/home/member/PycharmProjects/Boo-T/Zerg1.jpg,
	image=home/member/PycharmProjects/Boo-T/Zerg2.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg3.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg4.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg5.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg6.jpg) hullahopp

bootrow(rate(auto), 
	article(rawtext="Of course, you can wrap it into two rows, for your taste."
)) hullahopp

bootrow(rate(auto),  
	image=/home/member/PycharmProjects/Boo-T/Zerg1.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg2.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg3.jpg
) hullahopp

bootrow(rate(auto), 
	image=/home/member/PycharmProjects/Boo-T/Zerg4.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg5.jpg,
	image=/home/member/PycharmProjects/Boo-T/Zerg6.jpg) hullahopp

bootrow(rate(3,6,3),  
	image=/home/member/PycharmProjects/Boo-T/Zerg5.jpg,
	article(rawtext="But you can do it like this, where the column in the middle takes up twice the place."),
	image=/home/member/PycharmProjects/Boo-T/Zerg6.jpg) hullahopp

bootrow(rate(auto), 
	article(rawtext="<ul><li><b>article(title="", title-align=, rawtext="")</b></il><br>Articles are walls of text, the object you are reading right now is an arcticle as well. Articles have three part:<ul><li>title="String"</li>The text for the title, given as a string.<li><b>title-align</b>={left, center, right}<br>This will set the aligment of the title.</li><li><b>rawtext=""</b><br>This is the most advanced argument in the whole environment, this is the mathod for embending test. You can use here any html tags to make your text more pleasant for the eyes, here you can find some examples, I added some spaces so they won't be compiled:</li>< b > is for <b>bold</b> text, < i > is for <i>italic</i>, < u > stand for <u>underlined</u>. <br>You can add new lines by inserting a < br >, since normal enters won't work. You can create list by < ul > < ol > and itt items with < li >. I created a new tag that is not used by html standards: < space:X > will add X spaces to you text, < space:10 > works <space:10> like this-</ul><li><b>image</b>=<br>Works like as mentioned before.</li><li><b>imgfilter</b><br>This argument changes the image behavior by making it blurry and grayscale unit the mouse goes by.</li></ul>")) hullahopp

bootrow(rate(auto), image=/home/member/PycharmProjects/Boo-T/Zerg5.jpg,
	article(title="centered title", title-align=center,
	rawtext="This is a normal image, i have to write here some uninteresting thing to make it work.")) hullahopp

bootrow(rate(auto), image=/home/member/PycharmProjects/Boo-T/Zerg5.jpg, imgfilter,
	article(title="right-aligned title", title-align=right,
	rawtext="This one is filtered! Just showing you the basic syntax for a bootrow:<br><u>bootrow</u>(id=Two, rate(3,6,3), imgfilter,<br><space:20>image=05.jpg,<br<space:20>   article(title="This is the Title!", title-align=center,<br><spcae:20>rawtext="And this is some really awesome text!"),<br><space:20>image=06.jpg<br><space:20>) %%")) hullahopp

bootrow(id=tables, rate(auto), 
	article(title="VI. Tables", title-align=left, 
	rawtext="Tables are a little oldschool, but can give your visitors many information collected into a small place. They are invoked with the <u>table</u>() command, and there are additional fields to fill them with content:<ul><li><b>id=</b><br>Same as the bootrow.</il><li><b>columns("string","string","string")></b><br>You have to add the columns names as a list of strings.</li><li><b>row("string","string","string")<b><br>You add rows with a single subcommand that contains a list of strings</li><li><b>inverted</b><br>Will let you change the colors of the table, it may be easier to read that way!</li></ul>So the syntax of the example tables looks like this:<br><u>table</u>(id=Protoss, columns("Unit","HP/Shield","Mana","Mineral","Gas"),<br><space:20>row("Zealot","100/60","0","100","0"),<br><space:20>row("Dragoon","100/80","0","125","50"),<br><space:20>row("High Templar","40/40","250","50","150"),<br><space:20>row("Dark Templar","80/40","0","125","100")<br>The second one has the "inverted" argument added!)")) hullahopp

table(id=Protoss1, columns("Unit","HP/Shield","Mana","Mineral","Gas"),
      row("Zealot","100/60","0","100","0"),
      row("Dragoon","100/80","0","125","50"),
      row("High Templar","40/40","250","50","150"),
      row("Dark Templar","80/40","0","125","100") hullahopp

table(id=Protoss2, inverted, columns("Unit","HP/Shield","Mana","Mineral","Gas"),
      row("Zealot","100/60","0","100","0"),
      row("Dragoon","100/80","0","125","50"),
      row("High Templar","40/40","250","50","150"),
      row("Dark Templar","80/40","0","125","100") hullahopp
) hullahopp

bootrow(id=footer, rate(auto), 
	article(title="VII. Footer", title-align=left, 
	rawtext="Footers are showing the user where they can contact you, so they are really important to make. Footers in Boo-T are prebaked, so you don't have to worry about it. Footers are created with the <u>Footer()</u> command and basically, you have to enter two kind of arguments. The button will scroll back to the top and on smaller screens, it will be attached to the bottom. Also, the Footer contains a lot of buttons to social media.<ul><li><b>button="String"</b><br>You can add the text to the button as a string.<li><b>{media}=</b><br>You can add a social media icon and your desired link. Media can be email, phone, skype, facebook, youtube, instagram, vkontakte, googleplus, linkedin, twitter or github.</li>The footer of this site looks like this:<br>footer(button="Scroll back to top!",<br><space:20>facebook=https://www.facebook.com/jnszltn.fhr/,<br><space:20>email=feher.janos.zoltan@gmail.com,<br><space:20>phone=+36705977991,<br><space:20>github=https://github.com/MemberA2600,<br><space:20>youtube=https://www.youtube.com/user/M3MB3Rrr,<br><space:20>linkedin=https://www.linkedin.com/in/j%C3%A1nos-zolt%C3%A1n-feh%C3%A9r-4378828b/) ")) hullahopp

footer(button="Scroll back to top!",
	facebook=https://www.facebook.com/jnszltn.fhr/,
	email=feher.janos.zoltan@gmail.com,
	phone=+36705977991,
	github=https://github.com/MemberA2600,
	youtube=https://www.youtube.com/user/M3MB3Rrr,
	linkedin=https://www.linkedin.com/in/j%C3%A1nos-zolt%C3%A1n-feh%C3%A9r-4378828b/) hullahopp





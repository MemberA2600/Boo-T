basics(author=Member,
       language=hu, 
       palette=1) %%

keywords(Feh�r J�nos Zolt�n, Member, Atarian) %%
description(Csak egy weblap) %%
title(�n) %%

background(image=D:/Archieve-Copy/MEMBER/chess.gif) %%
font-family(Impact) %%

banner(image=D:/Archieve-Copy/MEMBER/Atari/One-Player-Pong-Featured.jpg,
	text("Atari is cool!", 5em, left),
	height=250) %%

navbar(brand("MEMBER!!"), 
       item("R�lam", rolam),
       item("Atari2600 k�pek", Atari1),
       item("Atari2600 le�r�s", Atari2),
       item("T�bl�zat", AtariTable),
       item("El�rhet�s�g", Footer),
       opacity=0.75,
       sticky) %%

bootrow(id=rolam, rate(7,5), opacity=0.75,
    image=D:/Archieve-Copy/MEMBER/tvben.png, imgfilter,
    article(artitle="Ki vagyok �n?", title-align=right,
    rawtext="Magam sem tudom, azt pedig f�leg nem, hogy mi�rt �ppen <b>webes<b> szakdolgozatot v�lasztottam, els�re nagyon ijeszt�, de <b><u>m�sodj�ra</u></b> is!")) %%

bootrow(id=Atari1, rate(auto),
    image=D:/Archieve-Copy/MEMBER/Atari/atari_2600_bois_4_switch__secam__french__model_as_by_lulrik-d8tqv8m.jpg,
    image=D:/Archieve-Copy/MEMBER/Atari/great_beyond_atari_2600.jpg()(30BD3B8E0836CF22A74541143ABBC1E1).jpg,
    image=D:/Archieve-Copy/MEMBER/Atari/atari26000.png,
    image=D:/Archieve-Copy/MEMBER/Atari/mkatariwp.jpg) %%

bootrow(id=Atari2, rate(3,6,3), imgfilter,
   image=D:/Archieve-Copy/MEMBER/Atari/Crazy monkey.jpg,
   article(artitle="Atari2600!!!", title-align=center, rawtext="A legki�lyabb videoj�t�k-konzol 1977-b�l, ami becsemp�szte lak�sodba a videoj�t�k �lm�nyt!"),
   image=D:/Archieve-Copy/MEMBER/Atari/2017-06-14-keithrobinsonb.jpg
 ) %%

table(id=AtariTable, opacity=0.75,inverted,
      columns("J�t�k neve", "Gy�rt�", "�v"),
      row("Air-Sea Battle", "Atari Inc.", "1977"),
      row("Dig-Dug", "Namco", "1983"),
      row("Ikari Warriors", "Atari Inc.", "1989"),
      row("Donkey Kong", "Nintendo", "1982")
      ) %%

footer(id=Footer,opacity=0.75,
       button="GO BACK",
       facebook=https://www.facebook.com/AtariHungary/,
       github=https://github.com/MemberA2600/PublicForLinkedin,
       youtube=https://www.youtube.com/user/M3MB3Rrr,
       linkedin=https://hu.linkedin.com/in/j%C3%A1nos-zolt%C3%A1n-feh%C3%A9r-4378828b
	) %%










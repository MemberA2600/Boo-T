deliminator pacal (1)
basics(
	author=Fehér János Zoltán,
       	language=hu, 
       	charset=utf-8,
       	palette=gray
	) pacal (2)

keywords(Neumann János,informatika,kibernetika,fejlődés) pacal (3)
description(Rövid weboldal Neumann Jánosról az OKJ záróvizsga védés céljából) pacal (4)
title(Neumann János) pacal (5)

opacity(navbar=0.85, container=0.85, table=0.85, footer=0.85) pacal (6)

background(image=img/circuit.jpg) pacal (7)
font-family("Myriad Pro Light", "Tahoma") pacal (8)

banner(
	text("Neumann János", 3em, center),
	size=cover,
	height=400,
	animation(10s, 
		img/neumann1.jpg,
		img/neumann2.jpg,
		img/neumann3.jpg
		)
	) pacal (9)

navbar(
	brand(image=img/arc.svg),
	sticky,
	expand=md,
	item("Élete", eletut),
	item("Neumann-Elvek", elvek),
	item("Művei", muvei),
	item("Galéria", galeria)
	) pacal (10)

bootrow(
	id=eletut,
	rate(9,3),
	article(	title="Élete",
		title-align=left,
		rawtext="<b>1903. december 28</b>-án született Budapesten, jómódú családból. Apja <i>Neumann Miksa</i> bankár, anyja Kann Margit.<br>
Két öccse született: <i>Mihály</i> (1907), chicagói orvos és <i>Miklós</i> (1911), philadelphiai jogász. Apja, Miksa a város magánbankjainak egyik résztulajdonosa volt, így gyermekei számára az anyagi jólét mellett a szellemi hátteret is bírta nyújtani. 1903-ban <b>Ferenc József</b> magyar király nemesi rangot ad a családnak, és felvehetik a Margittai előnevet. Később Amerikában a <b>John von Neumann</b> nevet használta, de Johnnynak vagy Jancsinak hívták barátai."
		),
	image=img/foto.jpg
	) pacal (11)

bootrow(
	id=elvek,
	rate(3,6,3),
	image=img/neumann-gep.png,
	article(	title="Neumann-elvek",
		title-align=left,
		rawtext="<ul><li>A számítógép legyen teljesen elektronikus, külön vezérlő és végrehajtóegységgel rendelkezzen</li><li>Kettes számrendszert használjon</li><li>Az adatokat és a programokat ugyanabban a belső tárban, a memóriában legyenek</li><li>A számítógép legyen univerzális Turing-gép
</li></ul>"
	),
	image=img/eniac.jpg
	) pacal (12)

table(
	id=muvei,
	columns("Szerzők","Cím","Kiadó","Kiadás Éve"),
	row("Aspray, William","Neumann János és a modern számítástechnika kezdetei","Vince Kiadó","2004"),
	row("Marx György","A marslakók érkezése","Akadémiai Kiadó","2000"),
	row("Szanton, Andrew", "Wigner Jenő emlékiratai", "Kairosz Kiadó", "2002"),
	row("Teller Ede", "Huszadik századi utazás tudományban és politikában", "XX. Század Intézet", "1987")
	) pacal (13)

bootrow(	id=galeria,
	rate(auto),
	image=img/01.png,
	image=img/02.jpg,
	image=img/03.jpg,
	image=img/04.jpg,
        	imgfilter
	) pacal (14)

footer(	
	button="Görgess vissza!", 
	facebook=#,
	linkedin=#,
	youtube=#,
	github=#
) pacal (15)





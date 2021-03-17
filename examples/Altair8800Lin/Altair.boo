basics(author=Member - Fehér János Zoltán,
       language=en, 
       charset=UTF-8,
       palette=7) %%

keywords(Altair 8800,70s computing, vintage, computer science) %%
description(Just a simple site dedicated to the Altair 8800 computer) %%
title(Altair 8800) %%
background(gradient=HOR) %%
font-family("Gulim") %%pic

banner(animation(40s, src/01.jpg,
		    src/02.jpg,
		    src/03.jpg,
		    src/04.jpg,
		    src/05.jpg),
       text("Altair 8800", 8em, center),
       height=300) %%

navbar(brand(image=src/mits.svg), sticky,
	item("The Hardware", hw),
	item("Programing", prog),
	item("Gallery", pic),
	item("Price", price)
	) %%

bootrow(id=hw, rate(7,5), article(
	title="Hardware", title-align=left, rawtext=
	"The Altair 8800 from Micro Instrumentation Telemetry Systems (MITS) of Albuquerque, NM, is considered by many to be the first personal computer - a computer that is easily affordable and obtainable. The entire Altair 8800 system is comprised of a metal case, a power supply, a front panel with switches, and a passive motherboard with expansion slots. All of the circuitry - the CPU and memory, are on cards which plug into the expansion slots, which MITS called the Altair Bus."), 
	image=src/07.jpg) %%

bootrow(id=prog, rate(7,5), article(
	title="Programming", title-align=left, rawtext=
	"The ALTAIR 8800 has 78 basic machine language instructions. Since many of the instructions can be modified to affect different registers or register pairs, more than 200 variances of the basic instructions are possible. Each instruction is presented as a standardized mnemonic or machine language code. Instructions may occupy from one to three sequential (serial) bytes, and the appropriate bit patterns are included. A condensed summary of the complete instruction set showing the mnemonics and instructions in both binary and octal is included as an Appendix."), 
	image=src/09.png) %%

bootrow(id=pic, rate(auto),
        image=src/10.jpg,
        image=src/11.jpg,
        image=src/12.jpg) %%

bootrow(rate(auto),
        image=src/13.jpg,
        image=src/14.jpg,
        image=src/16.jpg) %%

table(id=price, columns("Function", "Kit", "Assembled"), inverted,
	row("1K static RAM", "$97", "$139"),
	row("2K static RAM", "$145", "$195"),
	row("4K static RAM", "$195", "$275"),
	row("Serial Interface", "$119", "$139"),
	row("Paralell Interface", "$92", "$114"),
	row("Casette Interface", "$128", "$175")
) %%



footer(button="Keyboard is for dummies!",
       facebook=https://www.facebook.com/groups/265721677918/,
       youtube=https://www.youtube.com/channel/UC1y5UrhN90ULLSGnZjzR7Fw,
       skype=#,
       phone=#,
       email=grant@stockly.com )%%




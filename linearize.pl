#!/usr/bin/perl -w
###################################
# Linearlize all latex files into a single file. 
#  - strips lines that start with %
#  - paragraph on a single line (necessary for including in word)
#
# Usage 
#   ./scripts/linearize (word|acm) <top-file.tex>
#
# Mode #1 - output for inclusion into Word (spell check)
#  - remove Citations, labels and refs
#  
# Mode #2 - inlining for TOCS submission
#  - inlines the bibliography (todo) 
#  - renumbers the figures (todo)
##################################
use strict;

my @SKIPFILES = ("epsf.tex");
my $option;
my $figureCount = 1;
my %label;
my %bibitem;

sub FindCommand {
    my $p = shift;
    my $cmd = shift;
    my $pos = shift;
    my $x = index($p,"\\".$cmd."{",);
    return $x;
}

    
    
sub ClosingBrace {
    my $p = shift;
    my $pos = shift;    
    my $count = 1;
    substr($p,$pos,1) eq "{" || die "not an opening brace \n";

    $pos++;
    while ($pos < length($p)) {
	my $c = substr($p,$pos,1);
	if ($c eq "{") { 
	    $count++;
	} elsif ($c eq "}") {
	    $count--;
	    if ($count == 0) { 
		return $pos;
	    }
	}
	$pos++;
    }
    return -1;
}

# drop the the command, e.g. \emph{foo} --> foo
sub DropCommand {
    my $p = shift;
    my $command = shift;
    my $end;
    my $start;
    my $openbrace;

    while (($start=index($p,$command."{"))>=0) {
	print  "found $command\n";
	$openbrace = $start + length($command);
	$end =  ClosingBrace($p,$openbrace);
	$end >0 || die "assert no end for $command\n";
	$p = substr($p,0,$start) .substr($p,$openbrace+1,$end-$openbrace-1). substr($p,$end+1);
    }
    return $p;
}


## -> \cite{foo} --> [CITE]
sub ReplaceCommand {
    my $p = shift;
    my $command = shift;
    my $repl = shift;
    my $end;
    my $start;
    my $openbrace;
    
    while (($start =  index($p,$command."{"))>=0) {
	$end = index($p,"}",$start+1);
	$end >0 || die "assert no end\n";
	my $restart = $end+1;
	# if it ends with a \n, then skil the trailing blanks (required)
	while (index($repl,"\n")>=0 && substr($p,$restart,1) eq " ") {
	    $restart++;
	}

	$p = substr($p,0,$start) . $repl . substr($p,$restart);
    }
    return $p;
}

sub ReplaceString {
    my $p = shift;
    my $command = shift;
    my $repl = shift;
    my $start;
    my $end;
    while (($start =  index($p,$command))>=0) {
	$end = $start + length($command);
	$p = substr($p,0,$start) . $repl . substr($p,$end);
    }
    return $p;
}
    

# -->\section{Hello} --> .SE "Hello"\n    

sub Roff {
    my $p = shift;
    my $command = shift;
    my $replA = shift;
    my $replB = shift;
    my $end;
    my $start;
    my $openbrace;
    
    while (($start =  index($p,$command))>=0) {
	print "ROFF $command\n";
	$openbrace = $start + length($command);
	$end = index($p,"}",$start+1);
	$end >0 || die "assert no end\n";
	my $restart = $end+1;
	# if it ends with a \n, then skil the trailing blanks (required)
	while (index($replB,"\n")>0 && substr($p,$restart,1) eq " ") {
	    $restart++;
	}
	$p = substr($p,0,$start) . $replA  .substr($p,$openbrace,$end-$openbrace). $replB . substr($p,$restart);
    }
    return $p;
}
    
sub RoffAUX { 
    my $p = shift;
    my $command = shift;
    my $namespace = shift;
    my $end;
    my $start;
    my $openbrace;
    my $x;

    while (($start =  index($p,$command."{"))>=0) {
	print "ROFF $command\n";
	$openbrace = $start + length($command);
	$end = index($p,"}",$start+1);
	$end >0 || die "assert no end\n";
	if ($namespace eq "label") { 
	    $x = $label{substr($p,$openbrace+1,$end-$openbrace-1)};
	    if (!defined($x)) { 
		die "LABEL ". substr($p,$openbrace+1,$end-$openbrace-1)." not defined\n";
	    }
	} elsif ($namespace eq "bibitem") {
	    $x = substr($p,$openbrace+1,$end-$openbrace-1);
	    if ($x =~/,/) { 
		my @xx = split(",",$x);
		my $i;
		for $i (0..$#xx) { 
		    $xx[$i] = $bibitem{$xx[$i]};
		}
		$x = "(".join(",",@xx).")";
	    } else {
		$x = "(".$bibitem{$x}.")";
	    }
	    if (!defined($x)) { 
		die "BIBITEM ". substr($p,$openbrace+1,$end-$openbrace-1)." not defined\n";
	    }
	    
	} else {
	    die "bad option\n";
	}

	$p = substr($p,0,$start) . $x . substr($p,$end+1);
    }
    return $p;
}

    

sub Spill {
    my $p = shift;
    my $start;
    my $openbrace;
    my $end;
    my $end2;
    my $start2;

    if ($p eq "") {
	# skip
    } else {
	## transmutate
	## 

	### all versions. 
	while (($start=index($p,"\\thesisarticle{"))>=0) {
	    # keep article; drop thesis version
	    $openbrace = $start + length("\\thesisarticle");
	    $end =  ClosingBrace($p,$openbrace);
	    $end >0 || die "assert no end\n";
	    $end2 = ClosingBrace($p,$end+1);
	    $p = substr($p,0,$start) .  substr($p,$end+2,$end2-$end-2) .substr($p,$end2+1);
	}
	

	my $tobreak = 1;
	while ($tobreak && ($start=index($p,"\\thesisonly{"))>=0) {
	    # keep article; drop thesis version
	    $openbrace = $start + length("\\thesisonly");
	    $end =  ClosingBrace($p,$openbrace);
	    if ($end<=0) { 
		print STDERR "Could not removed \\thesisonly\n";
		$tobreak = 0;
	    } else {
		$p = substr($p,0,$start) .  substr($p,$end+1);
	    }
	}

	if ($option eq "word") { 

	    $p = ReplaceCommand($p,"~\\cite"," [CITE]");
	    $p = ReplaceCommand($p,"~\\ref", " [REF]");
	    $p = ReplaceCommand($p,"\\S\\ref","[SECREF]");
		$p = ReplaceCommand($p,"\\sout","");
		$p = ReplaceCommand($p,"\\autoref","[AUTOREF]");


	    while (($start=index($p,"~\\citeName{"))>=0) {
		$openbrace = $start + length("~\\citeName");
		$end =  ClosingBrace($p,$openbrace);
		$end >0 || die "assert no end\n";
		$end2 = ClosingBrace($p,$end+1);
		print STDERR "CiteName ".substr($p,$end,$end2-$end-2) . "\n";
		$p = substr($p,0,$start) . " [CITENAME]" . substr($p,$end2+1);
	    }

	    # keep 2nd arg
	    while (($start=index($p,"\\camera{"))>=0) {
		$openbrace = $start + length("\\camera");
		$end =  ClosingBrace($p,$openbrace);
		$end >0 || die "assert no end\n";
		$end2 = ClosingBrace($p,$end+1);
		print STDERR "Camrea ".substr($p,$end+2,$end2-$end-2) . "\n";
		$p = substr($p,0,$start) . " ".substr($p,$end+2,$end2-$end-2) . " ".substr($p,$end2+1);
	    }
	    
	    $p = DropCommand($p,"\\emph");
	    $p = DropCommand($p,"\\texttt");
	    $p = DropCommand($p,"\\textit");


	    $p = ReplaceCommand($p,"\\label"," [LABEL]");
	    $p = ReplaceCommand($p,"\\includegraphics"," [PICTURE]");
	    $p = ReplaceCommand($p,"\\ignore","");
	    $p = ReplaceCommand($p,"\\edb","");

		$p = ReplaceString($p,"\\eg~","e.g., ");
		$p = ReplaceString($p,"\\ie~","i.e., ");
		$p = ReplaceString($p,"\\eg","e.g.,");
		$p = ReplaceString($p,"\\ie","i.e.,");
		$p = ReplaceString($p,"\\etc","etc.,");
		$p = ReplaceString($p,"\\etal","et al.");
		

		$p = ReplaceString($p,"\\noindent","");
		$p = ReplaceString($p,"\\centering","");
		$p = ReplaceString($p,"\\item","\n[ITEM:]"); 
			
	} elsif ($option eq "acm") { 
	    while ($p =~/\\comment{/) { 
		$start = index($p,"\\comment{");
		$end = ClosingBrace($p,$start + length("\\comment"));
		if ($end>0) { 
		    $p = substr($p,0,$start) . substr($p,$end+1);
		} else {
		  last;
		}
	    }

	    while (($start=index($p,"\\edb{"))>=0) {
		$openbrace = $start + length("\\edb");
		$end =  ClosingBrace($p,$openbrace);
		$end >0 || die "assert no end\n";
		$p = substr($p,0,$start) . " " . substr($p,$end+1);
	    }

	    while (($start = index($p,"\\graphicsonecolumn{"))>=0) { 
		$openbrace = $start + length("\\graphicsonecolumn");
		$end =  ClosingBrace($p,$openbrace);
		$end >0 || die "assert no end\n";
		
		print STDERR "Figure $figureCount:: " . substr($p,$openbrace+1,$end-$openbrace-1) . "\n";

		$p = substr($p,0,$start) . "\\centerline{\\includegraphics{vmware-tocs" . "$figureCount" .
		    ".eps}}\n " . substr($p,$end+1);


		$figureCount++;
	    }
    	} elsif ($option eq "roff") {

	    #$p = DropCommand($p,"\\emph");

	    # \figurecaption{FIG}{CAPTION}{LABEL}

	    while (($start=index($p,"\\figurecaption{"))>=0) {
		$openbrace = $start + length("\\figurecaption");
		$end =  ClosingBrace($p,$openbrace);
		$end >0 || die "assert no end\n";
		$end2 = ClosingBrace($p,$end+1);
		my $end3 = ClosingBrace($p,$end2+1);
		my $figcaption_fig = substr($p,$openbrace+1,$end-$openbrace-1);
		my $figcaption_cap = substr($p,$end+2,$end2-$end-2);
		#my $figcaption_lab = 
		my $figcaption_w = "\n.BF 0\n.F+\nfigure ".$figcaption_fig."\n.F-\n.FC C\n".$figcaption_cap."\n.EF\n";

		print STDERR "[FIG CAPTION |".$figcaption_fig . "|".$figcaption_cap."]\n";

		$p = substr($p,0,$start) . $figcaption_w . substr($p,$end3+1);
	    }


	    $p = ReplaceCommand($p,"\\label","");
	    $p = ReplaceCommand($p,"\\ignore","");
	    $p = ReplaceCommand($p,"\\edb","");
	    $p = Roff($p,"\\section{",".SE \"","\"\n");
	    $p = Roff($p,"\\subsection{",".SS \"","\"\n");
	    $p = Roff($p,"\\paragraph*{",".UU \n","\n");

	    $p = Roff($p,"\\emph{","\n.KW \"","\"\n");
	    
	    $p = RoffAUX($p,"\\S\\ref","label");
	    $p = RoffAUX($p,"~\\cite","bibitem");

	    $p = ReplaceCommand($p,"\\prevref", "\n.PF\n");
	    $p = ReplaceCommand($p,"\\nextref", "\n.NF\n");


	    $p = ReplaceString($p,"\\begin{itemize}",".LI o\n");
	    $p = ReplaceString($p,"\\end{itemize}",".LX\n");

	    $p = ReplaceString($p,"\\begin{enumerate}",".LI o\n");
	    $p = ReplaceString($p,"\\end{enumerate}",".LX\n");
	    
	    $p = ReplaceString($p,"\\item",".IT\n");
	    
	    $p = Roff($p,"{\\bf ","\n.I \"","\"\n");
	    $p = Roff($p,"{\\tt ","\n.KW \"","\"\n");  # like KW (\emph)

	    $p = ReplaceString($p,"\\noindent","");
        $p = ReplaceString($p,"\\item","\n[ITEM:] ");
	    $p =~ s/~/ /g;
	}



	### recursive inclusion
	while (1) { 
	    $start = FindCommand($p,"input");
	    if ($start<0) { 
		last;
	    }
	    $openbrace = $start + 1 + length("input");
	    $end = ClosingBrace($p,$openbrace);
	    ($end >0) || die "assert";
	    if ($start>0) { 
		print OUT substr($p,0,$start-1);
	    }
	    my $inputfile = substr($p,$openbrace+1,$end-$openbrace-1);

		my $extension = index($inputfile,".tex");
		if ($extension>0) { 
			$inputfile = substr($inputfile,0,$extension);
			print "XXX TRIM inputfile $inputfile\n";
		}

	    $p = substr($p,$end+1); #remaining paragraph
	    print STDERR "Including $inputfile\n";
	    if ($option ne "roff")  {
		print OUT "\n\n%LATEX FILE $inputfile\n\n";
	    }
	    Linearize($inputfile . ".tex");
	    if ($option ne "roff")  {
		print OUT "\n\n%LATEX FILE $inputfile END\n\n";
	    }
	}

	if ($option eq "roff") {
	    if ($p ne "" && substr($p,0,1) ne ".") {
		print OUT ".PP\n";
	    }
	}
	print OUT $p;
	print OUT "\n\n";
    }
}


sub Linearize {
    my $f = shift;
    my $nlines = 0;
    my $i;
    my $line;

    for $i (@SKIPFILES) { 
	if ($f eq $i) { 
	    return;
	}
    }

    print "Linearize $f\n";


    open (F, $f) || die "could not open $f\n";
    my $paragraph = "";
    my @alllines;
    
    # read at once; allow recursion
    while (<F>) {	
	 $alllines[$nlines++] = $_;
    }
    close(F);

    for ($i=0;$i<$nlines;$i++) { 
	$line = $alllines[$i];
	chop($line);
	#print STDERR "XXX line=$line\n";
	### remove comment at end of lines
	### bug - misses % on a line that has an \% first
	my $x = index($line,"%",0);
	if ($x>=0) {
	    if ($x==0) { 
		$line = "";  #blank
	    } elsif (index($line,"\\%",0) <0) { 
		$line = substr($line,0,$x);
	    } else {
		# \% - rare
		print STDERR "comment\% ; kept it\n";
	    }
	}

	### remove trailing blanks
	while (substr($line,length($line)-1,1) eq " ") {
	    $line = substr($line,0,length($line)-1);
	}
	if (length($line) >0) { 
	    #### remove leading blanks
	    while (substr($line,0,1) eq " ") { 
		$line = substr($line, 1,length($line)-1);
	    }
	}
	
	if (length($line)==0) { 
	    # blank lines are separators;
	    Spill($paragraph) ;
	    $paragraph = "";
	} elsif (substr($line,length($line)-2,2) eq "\\\\") {
	    # lines that end with \\ are separators
	    Spill($paragraph . " " . $line);
	    $paragraph = "";
	} else {
	    # concatenate; same paragraph
	    if ($paragraph eq "") { 
		$paragraph = $line;
	    } else { 
		$paragraph = $paragraph . " " . $line;
	    }
	}

    }
    Spill($paragraph);   
}

$option = shift;

if ($option eq "word") {
    print STDERR "Preparing for word output (spellcheck) \n";
} elsif ($option eq "acm") { 
    print STDERR "Preparing for ACM submission\n";
} elsif ($option eq "roff") {
    print STDERR "Preparing for 20th ROFF\n";
} else {
    die "not a valid option\n";
}

    

my $toplevel = shift;
if ($option eq "roff") {
    my $aux = $toplevel;
    $aux =~s/tex/aux/;
    open (AUX,$aux) || die "Could not open $aux\n";
    while (<AUX>) { 
	if (/\\newlabel{(\S+)}{{(\S+)}{(\S+)}}/) { 
	    print "AUX LABEL $1 | $2 | $3\n";
	    $label{$1} = $2;
	}
    }
    close(AUX);

    $aux = $toplevel;
    $aux =~s/tex/bbl/;
    open (AUX,$aux) || die " could not open bbl\n";
    while (<AUX>) { 
	if (/\\bibitem/) {
	    my $x = index($_,"]");
	    my $xa = substr($_,length("\\bibitem["),$x-length("\\bibitem["));
	    my $xb = substr($_,$x+2 );
	    chop($xb);
	    chop($xb);
	    $bibitem{$xb} = $xa;
	    print "AUX BIB $xa | $xb\n";
	}
    }
    close(AUX);
}

open (OUT,">latex-all.tex");
Linearize($toplevel);
close(OUT);

from typing import Dict, Any
import os,shutil,time
import subprocess


class LaTeXGenerator:
    def __init__(self):
        self.name = ''
        self.phone = ''
        self.email = ''
        self.github = ''
        self.website = ''
        self.linkedin = ''
        self.location = ''
        self.latex_code = ''
        self.base_template = r"""

        \documentclass[10pt, letterpaper]{article}

        % Packages:
        \usepackage[
            ignoreheadfoot, % set margins without considering header and footer
            top=2 cm, % seperation between body and page edge from the top
            bottom=2 cm, % seperation between body and page edge from the bottom
            left=2 cm, % seperation between body and page edge from the left
            right=2 cm, % seperation between body and page edge from the right
            footskip=1.0 cm, % seperation between body and footer
            % showframe % for debugging 
        ]{geometry} % for adjusting page geometry
        \usepackage{titlesec} % for customizing section titles
        \usepackage{tabularx} % for making tables with fixed width columns
        \usepackage{array} % tabularx requires this
        \usepackage[dvipsnames]{xcolor} % for coloring text
        \definecolor{primaryColor}{RGB}{0, 0, 0} % define primary color
        \usepackage{enumitem} % for customizing lists
        \usepackage{fontawesome5} % for using icons
        \usepackage{amsmath} % for math
        \usepackage[
            pdftitle={John Doe's CV},
            pdfauthor={Palthi Malleswari},
            pdfcreator={LaTeX with RenderCV},
            colorlinks=true,
            urlcolor=primaryColor
        ]{hyperref} % for links, metadata and bookmarks
        \usepackage[pscoord]{eso-pic} % for floating text on the page
        \usepackage{calc} % for calculating lengths
        \usepackage{bookmark} % for bookmarks
        \usepackage{lastpage} % for getting the total number of pages
        \usepackage{changepage} % for one column entries (adjustwidth environment)
        \usepackage{paracol} % for two and three column entries
        \usepackage{ifthen} % for conditional statements
        \usepackage{needspace} % for avoiding page brake right after the section title
        \usepackage{iftex} % check if engine is pdflatex, xetex or luatex

        % Ensure that generate pdf is machine readable/ATS parsable:
        \ifPDFTeX
            \input{glyphtounicode}
            \pdfgentounicode=1
            \usepackage[T1]{fontenc}
            \usepackage[utf8]{inputenc}
            \usepackage{lmodern}
        \fi

        \usepackage{charter}

        % Some settings:
        \raggedright
        \AtBeginEnvironment{adjustwidth}{\partopsep0pt} % remove space before adjustwidth environment
        \pagestyle{empty} % no header or footer
        \setcounter{secnumdepth}{0} % no section numbering
        \setlength{\parindent}{0pt} % no indentation
        \setlength{\topskip}{0pt} % no top skip
        \setlength{\columnsep}{0.15cm} % set column seperation
        \pagenumbering{gobble} % no page numbering

        \titleformat{\section}{\needspace{4\baselineskip}\bfseries\large}{}{0pt}{}[\vspace{1pt}\titlerule]

        \titlespacing{\section}{
            % left space:
            -1pt
        }{
            % top space:
            0.3 cm
        }{
            % bottom space:
            0.2 cm
        } % section title spacing

        \renewcommand\labelitemi{$\vcenter{\hbox{\small$\bullet$}}$} % custom bullet points
        \newenvironment{highlights}{
            \begin{itemize}[
                topsep=0.10 cm,
                parsep=0.10 cm,
                partopsep=0pt,
                itemsep=0pt,
                leftmargin=0 cm + 10pt
            ]
        }{
            \end{itemize}
        } % new environment for highlights


        \newenvironment{highlightsforbulletentries}{
            \begin{itemize}[
                topsep=0.10 cm,
                parsep=0.10 cm,
                partopsep=0pt,
                itemsep=0pt,
                leftmargin=10pt
            ]
        }{
            \end{itemize}
        } % new environment for highlights for bullet entries

        \newenvironment{onecolentry}{
            \begin{adjustwidth}{
                0 cm + 0.00001 cm
            }{
                0 cm + 0.00001 cm
            }
        }{
            \end{adjustwidth}
        } % new environment for one column entries

        \newenvironment{twocolentry}[2][]{
            \onecolentry
            \def\secondColumn{#2}
            \setcolumnwidth{\fill, 4.5 cm}
            \begin{paracol}{2}
        }{
            \switchcolumn \raggedleft \secondColumn
            \end{paracol}
            \endonecolentry
        } % new environment for two column entries

        \newenvironment{threecolentry}[3][]{
            \onecolentry
            \def\thirdColumn{#3}
            \setcolumnwidth{, \fill, 4.5 cm}
            \begin{paracol}{3}
            {\raggedright #2} \switchcolumn
        }{
            \switchcolumn \raggedleft \thirdColumn
            \end{paracol}
            \endonecolentry
        } % new environment for three column entries

        \newenvironment{header}{
            \setlength{\topsep}{0pt}\par\kern\topsep\centering\linespread{1.5}
        }{
            \par\kern\topsep
        } % new environment for the header

        \newcommand{\placelastupdatedtext}{% \placetextbox{<horizontal pos>}{<vertical pos>}{<stuff>}
        \AddToShipoutPictureFG*{% Add <stuff> to current page foreground
            \put(
                \LenToUnit{\paperwidth-2 cm-0 cm+0.05cm},
                \LenToUnit{\paperheight-1.0 cm}
            ){\vtop{{\null}\makebox[0pt][c]{
                \small\color{gray}\textit{Last updated in September 2024}\hspace{\widthof{Last updated in September 2024}}
            }}}%
        }%
        }%

        % save the original href command in a new command:
        \let\hrefWithoutArrow\href
        """

        self.pernl_info = r"""
            \begin{{document}}
            \newcommand{{\AND}}{{\unskip
                \cleaders\copy\ANDbox\hskip\wd\ANDbox
                \ignorespaces
            }}
            \newsavebox\ANDbox
            \sbox\ANDbox{{$|$}}

            \begin{{header}}
                \fontsize{{25 pt}}{{25 pt}}\selectfont {{{name}}}

                \vspace{{5 pt}}

                \normalsize
                \mbox{{{location}}}%
                \kern 5.0 pt%
                \AND%
                \kern 5.0 pt%
                \mbox{{\hrefWithoutArrow{{mailto:{mail}}}{{mail}}}}%
                \kern 5.0 pt%
                \AND%
                \kern 5.0 pt%
                \mbox{{\hrefWithoutArrow{{tel:{phone}}}{{phone}}}}%
                \kern 5.0 pt%
                \AND%
                \kern 5.0 pt%
                \mbox{{\hrefWithoutArrow{{{website}}}{{website}}}}%
                \kern 5.0 pt%
                \AND%
                \kern 5.0 pt%
                \mbox{{\hrefWithoutArrow{{{linkedin}}}{{linkedin}}}}%
                \kern 5.0 pt%
                \AND%
                \kern 5.0 pt%
                \mbox{{\hrefWithoutArrow{{{github}}}{{github}}}}%
            \end{{header}}

            \vspace{{5 pt - 0.3 cm}}
        """
        
    def generate_section(self, section_name: str, fields: list) -> str:
        """Generate LaTeX code for a section"""

        section = [rf"\section{{{section_name}}} \begin{{onecolentry}} \begin{{highlightsforbulletentries}}"]

        for field in fields:
            section.append(rf"\item \textbf{{{field['field_name']}}}: {field['value']}")

        section.append(r"\end{highlightsforbulletentries} \end{onecolentry}")
        return "\n".join(section)

    
    def persnl_info_sec(self,section_name,fields):

        for field in fields:
            
            if field['field_name'] == 'Full Name':
                self.name = field['value']
            if field['field_name'] == 'Email':
                self.email = field['value']
            if field['field_name'] == 'Phone':
                self.phone = field['value']
            if field['field_name'] == 'Github Profile Link':
                self.github = field['value']
                

        

    def generate_latex(self, data: Dict[str, Any]) -> str:
        """Generate complete LaTeX document from form data"""
        sections_latex = ""
        
        # Generate each section
        for section_name, section_data in data.items():
            if section_name == 'Personal Information':
                self.persnl_info_sec(section_name,section_data)
            else:
                
                sections_latex += self.generate_section(
                    section_name,
                    section_data
                )
            
  
        # Replace placeholders in template
        latex_personal = self.pernl_info.format(
                name = self.name if self.name else "Palthi Malleswari",
                mail= self.email if self.email else "malleswaripalthi@gmail.com",
                phone=self.phone,
                github= self.github if self.github else "https://github.com",
                website="website",
                linkedin="https://linkedin//com",
                location="Macherla, Andhra Pradesh, India"
            )

        res = print(latex_personal)

        self.latex_code = self.base_template + latex_personal + sections_latex
        end_docs = """\end{document}"""
        self.latex_code += end_docs
        
        return self.latex_code

    def generate_begin_docs(self):
        st = r"""
        \begin{{document}}
    \newcommand{{\AND}}{{\unskip
        \cleaders\copy\ANDbox\hskip\wd\ANDbox
        \ignorespaces
    }}
    \newsavebox\ANDbox
    \sbox\ANDbox{{$|$}}

    \begin{{header}}
        \fontsize{{25 pt}}{{25 pt}}\selectfont John Doe

        \vspace{5 pt}

        \normalsize
        \mbox{{Location}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{{\hrefWithoutArrow{{mailto:mail}}{{mail}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{{\hrefWithoutArrow{{tel:phone}}{phone}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{{\hrefWithoutArrow{{profile}}{{profile}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{{\hrefWithoutArrow{{linkedin}}{{linkedin}}%
        \kern 5.0 pt%
        \AND%
        \kern 5.0 pt%
        \mbox{{\hrefWithoutArrow{{github}}{{github}}}%
    \end{header}}

    \vspace{5 pt - 0.3 cm}
        """
        self.latex_code += st.format(
            # name=self.name,
            email=self.email,
            phone=self.phone,
            location='Macherla, Andhra Pradesh, India',
            linkedin = "Linkedin",
            github = "Github",
            profilr="profile",
        )
        self.latex_code

    

    def generate_pdf(self, latex_code: str, output_path: str,output_file_name) -> bool:
        """Generate PDF from LaTeX code."""
        temp_tex = "temp_resume.tex"
        max_attempts = 3
        temp_pdf = "temp_resume.pdf"
        try:
            for ext in ['.aux', '.log', '.tex', '.pdf']:
                temp_file = f"temp_resume{ext}"
                if os.path.exists(temp_file):
                    os.remove(temp_file)

            # Write LaTeX to temporary file
            with open(temp_tex, "w") as f:
                f.write(latex_code)

            attempt = 0
  
            while attempt < max_attempts:
                result = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", temp_tex],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                # If pdflatex is successful, exit the loop
                if result.returncode == 0:
                    break

                attempt += 1
            print(f"Attempt {attempt} failed. Retrying...")

            # Check if pdflatex was successful
            if result.returncode != 0:
                    
                    print("pdflatex failed. Error output:")
                    print(result.stderr.decode())
                    print(result.stdout.decode()) 
                    # return False
            
            
            
            # Check if the PDF was generated
            if not os.path.exists(temp_pdf):
                print(f"PDF not generated: {temp_pdf}")
                return False

            os.makedirs(output_path, exist_ok=True)


            # Define the final destination path with the new filename
            final_pdf_path = os.path.join(output_path, output_file_name)

            # Move and rename the generated PDF
            shutil.move(temp_pdf, final_pdf_path)

            print(f"PDF successfully generated and moved to: {final_pdf_path}")
            return True

        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return False

        finally:
            # Cleanup temporary files
            for ext in ['.aux', '.log', '.tex', '.pdf']:
                temp_file = f"temp_resume{ext}"
                if os.path.exists(temp_file):
                    os.remove(temp_file)

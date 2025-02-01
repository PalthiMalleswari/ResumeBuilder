base_template = r"""
\documentclass[10pt, letterpaper]{{article}}

% Packages
\usepackage[
    top=2cm,
    bottom=2cm,
    left=2cm,
    right=2cm,
]{{geometry}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{fontawesome5}}
\usepackage[T1]{{fontenc}}

% Settings
\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}

% Custom section style
\titleformat{{\section}}{{\Large\bfseries}}{{}}{{0em}}{{[\titlerule]}}
\titlespacing{{\section}}{{0pt}}{{12pt}}{{6pt}}

\begin{{document}}

% Header
\begin{{center}}
    {{\Huge\bfseries {name}}}\\[0.5em]
    {{\small
        {location} $|$ 
        \href{{mailto:{email}}}{{{email}}} $|$ 
        {phone}
        % Add more contact details as needed
    }}
\end{{center}}

{sections}

\end{{document}}
"""

print(base_template)
sections = '\n\\section{Personal Information}\nrtyu\\\\\nasdfgh@gmail.com\\\\\n1234567890\\\\\n\nASDFGH\nhttps://leetcode.com/problems/jump-game/\\\\\nhttps://leetcode.com/problems/jump-game/\\\\\n\n\\section{Projects}\n\nsdfghjk\n\nsdfghjk\n\n\\section{Education}\n\nwertyhjk\n\nsdfgh\n\nqwerty\n\n\\section{Skills}\n\nsdfgh\n\nqwertyu\n\nasdfgh\n\nsdfgh\n\n\\section{Work Experience}\n\nwert\n\nsdfg\n\n\\section{Certifications}\n\nqwerty\n\nsdfg\n'
latex_code = base_template.format(
        name="Malli",
        email="lolll",
        phone="1234",
        location='Macherla, Andhra Pradesh, India',
        sections=sections)
print(latex_code)
import sys

sys.path.insert(1, "/home/qwertypi/mc-guesser")

from fix_formatting import format_question

cases = [
r"""
5. In the figure, the area of the trapezium is \(12 \text{ cm}^{2}\). Which of the following equations can be used to find \(x\)?<br/>
<img src="figures/5.svg" alt="5"><br/>
A. \(\dfrac{x(x+2)}{2}=12\).<br/>
B. \(x(x+2)=24\).<br/>
C. \(x^{2}-x(x-2)=12\).<br/>
D. \(x^{2}-x(x-2)=24\).
""",
r"""
17. The figure shows a rectangle inscribed in a circle. Find the area of the shaded region correct to the nearest \(0.1 \text{ cm}^2\). <img src="figures/17.svg" alt="Figure 17"><br/>
A. \(60.0 \text{ cm}^2\).<br/>
B. \(72.7 \text{ cm}^2\).<br/>
C. \(132.7 \text{ cm}^2\).<br/>
D. \(470.9 \text{ cm}^2\).
""",
r"""
6. Find the values of \(x\) which satisfy both \(x+3>0\) and \(-2x<1\).<br/>
A. \(x>-3\)<br/>
B. \(x>-\dfrac{1}{2}\)<br/>
C. \(x>\dfrac{1}{2}\)<br/>
D. \(-3<x<-\dfrac{1}{2}\)<br/>
E. \(-3<x<\dfrac{1}{2}\)
"""
]

for case in cases:
    print(format_question(case))

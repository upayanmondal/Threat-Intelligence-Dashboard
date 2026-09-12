from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(scan):

    filename = f"scan_{scan.id}.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize = A4
    )

    styles = getSampleStyleSheet()

    content = []

    # Report Title
    content.append(
        Paragraph("Threat Intelligence Report", styles["Title"])
    )

    content.append(Spacer(1, 20))

    # Target Information
    content.append(
        Paragraph(f"Target: {scan.target}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Target Type: {scan.target_type}", styles["Normal"])
    )

    content.append(Spacer(1, 20))

    # Risk Assessment
    content.append(
        Paragraph("Risk Assesment", styles["Heading2"])
    )

    risk = scan.results.get("Risk Score", {})

    content.append(
        Paragraph(f"Risk Score: {risk.get("Risk Score", "N/A")}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Risk Level: {risk.get("Risk Level", "N/A")}", styles["Normal"])
    )


    content.append(Spacer(1, 20))

    # AI Analysis
    content.append(Paragraph(f"AI Analysis", styles["Heading2"]))

    # Convert AI response into separate lines
    analysis = scan.ai_analysis

    for line in analysis.split("\n"):

        line = line.strip()

        if not line:
            content.append(Spacer(1, 8))
            continue
        
        # Remove Markdown Heading Symbols
        if line.startswith("###"):
            line = line.replace("###", "").strip()

            content.append(
                Paragraph(
                    line,
                    styles["Heading3"]
                )
            )

        # Remove Markdown * symbols
        elif line.startswith("*"):
            line = line.replace("*", "").strip()
            
            if ":" in line:
                indx = line.index(":")

                #for i in range(indx+1):
                till = line[0:indx+1]

                content.append(
                    Paragraph(
                        "-> " + till,
                        styles["Heading3"]
                    )
                )

                content.append(
                    Paragraph(
                        line[indx+1:],
                        styles["Normal"]
                    )
                )
            else:
                content.append(
                    Paragraph(
                        "-> " + line,
                        styles["Normal"]
                    )
                )


        # Remove Markdown horizontal symbols
        elif line == "---":
            content.append(Spacer(1, 5))
        
        else:
            content.append(
                Paragraph(
                    line,
                    styles["Normal"]
                )
            )


    doc.build(content)

    return filename

if __name__ == "__main__":
    print("PDF module is working Properly")
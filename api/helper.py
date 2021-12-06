def pdf_rotator(pdf_reader, pdf_writer, page_to_be_rotated, angle_of_rotation):
    for pagenum in range(pdf_reader.numPages):
        page = pdf_reader.getPage(pagenum)
        if pagenum + 1 == int(page_to_be_rotated):
            page.rotateClockwise(angle_of_rotation)
        pdf_writer.addPage(page)

    pdf_out = open('rotated.pdf', 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()


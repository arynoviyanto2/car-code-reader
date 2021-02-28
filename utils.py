import bs4


def hocr_character_parser(hocr):
    soup = bs4.BeautifulSoup(hocr, 'html.parser')

    characters = []

    page = soup.find("div", {"class": "ocr_page"})
    while page is not None:
        # Info in page level
        page_id = page.get("id")
        pg_summary = [info.strip() for info in page.get("title").split(";")]
        pg_x1, pg_y1, pg_x2, pg_y2 = map(int, pg_summary[1].split("bbox ")[1].split())

        area = page.findChild("div", {"class": "ocr_carea"})
        while area is not None:
            # Info in area level
            area_id = area.get("id")
            a_summary = [info.strip() for info in area.get("title").split(";")]
            a_x1, a_y1, a_x2, a_y2 = map(int, a_summary[0].split("bbox ")[1].split())

            paragraph = area.findChild("p", {"class": "ocr_par"})
            while paragraph is not None:
                # Info in paragraph level
                paragraph_id = paragraph.get("id")
                p_summary = [info.strip() for info in paragraph.get("title").split(";")]
                p_x1, p_y1, p_x2, p_y2 = map(int, p_summary[0].split("bbox ")[1].split())

                line = paragraph.findChild("span", {"class": "ocr_line"})
                while line is not None:
                    # Info in line level
                    line_id = line.get("id")
                    l_summary = [info.strip() for info in line.get("title").split(";")]
                    l_x1, l_y1, l_x2, l_y2 = map(int, l_summary[0].split("bbox ")[1].split())
                    # there are more; may be needed in the future

                    word = line.findChild("span", {"class": "ocrx_word"})
                    while word is not None:
                        # Info in word level
                        word_id = word.get("id")
                        w_summary = [info.strip() for info in word.get("title").split(";")]
                        w_x1, w_y1, w_x2, w_y2 = map(int, w_summary[0].split("bbox ")[1].split())
                        w_conf = float(w_summary[1].split("x_wconf ")[1])

                        character = word.findChild("span", {"class": "ocrx_cinfo"})
                        while character is not None:
                            # Info in character level
                            summary = [info.strip() for info in character.get("title").split(";")]
                            x1, y1, x2, y2 = map(int, summary[0].split("x_bboxes ")[1].split())
                            conf = float(summary[1].split("x_conf ")[1])
                            text = character.getText()

                            c_obj = {
                                'text': text,
                                'conf': conf,
                                'bbox': (x1, y1, x2, y2),
                                'word_id': word_id,
                                'word_bbox': (w_x1, w_y1, w_x2, w_y2),
                                'word_conf': w_conf,
                                'line_id': line_id,
                                'line_bbox': (l_x1, l_y1, l_x2, l_y2),
                                'paragraph_id': paragraph_id,
                                'paragraph_bbox': (p_x1, p_y1, p_x2, p_y2),
                                'area_id': area_id,
                                'area_bbox': (a_x1, a_y1, a_x2, a_y2),
                                'page_id': page_id,
                                'page_bbox': (pg_x1, pg_y1, pg_x2, pg_y2)
                            }

                            characters.append(c_obj)

                            character = character.findNextSibling("span", {"class": "ocrx_cinfo"})
                        word = word.findNextSibling("span", {"class": "ocrx_word"})
                    line = line.findNextSibling("span", {"class": "ocr_line"})
                paragraph = paragraph.findNextSibling("p", {"class": "ocr_par"})
            area = area.findNextSibling("div", {"class": "ocr_carea"})
        page = soup.findNextSibling("div", {"class": "ocr_page"})

    return characters


def get_text(characters):
    pass

import fitz
import os


class ImageExtractor:

    def extract_images(self, pdf_path, output_folder):

        os.makedirs(output_folder, exist_ok=True)

        doc = fitz.open(pdf_path)

        extracted_images = []

        for page_num in range(len(doc)):

            page = doc[page_num]

            images = page.get_images(full=True)

            for img_index, img in enumerate(images):

                xref = img[0]

                base_image = doc.extract_image(xref)

                width = base_image["width"]
                height = base_image["height"]

                # Ignore tiny image fragments
                if width < 100 or height < 100:
                    continue

                image_bytes = base_image["image"]

                image_ext = base_image["ext"]

                image_name = (
                    f"page_{page_num + 1}_image_{img_index + 1}.{image_ext}"
                )

                image_path = os.path.join(
                    output_folder,
                    image_name
                )

                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                extracted_images.append(
                    {
                        
                        "page_number": page_num + 1,
                        "image_name": image_name,
                        "image_path": image_path,
                        "width": base_image["width"],
                        "height": base_image["height"]
                    }
                )

        doc.close()

        return extracted_images
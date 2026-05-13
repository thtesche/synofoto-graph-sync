from PIL import Image
from PIL.ExifTags import TAGS
import logging
import os

logger = logging.getLogger(__name__)

class XMPParser:
    @staticmethod
    def extract_tags(file_path):
        """
        Extracts keywords/tags from image metadata.
        Supports standard EXIF and attempts to find XMP data.
        """
        tags = []
        if not os.path.exists(file_path):
            return tags

        try:
            with Image.open(file_path) as img:
                # Basic EXIF
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        # XPKeywords is often used by Windows/Synology for tags
                        if tag == 'XPKeywords' and isinstance(value, bytes):
                            tags.extend(value.decode('utf-16').split(';'))
                
                # Check for XMP in info (Pillow stores it there for some formats)
                if hasattr(img, 'info') and 'xmp' in img.info:
                    xmp_data = img.info['xmp']
                    # Simple string searching for common tag patterns if XML parsing is too heavy
                    # Realistically, we should use an XML parser here
                    import re
                    # Match <dc:subject>...</dc:subject> or <lr:hierarchicalSubject>...</lr:hierarchicalSubject>
                    subjects = re.findall(r'<dc:subject>.*?</dc:subject>', xmp_data.decode('utf-8'), re.DOTALL)
                    for sub in subjects:
                        items = re.findall(r'<rdf:li>(.*?)</rdf:li>', sub)
                        tags.extend(items)
        except Exception as e:
            logger.error(f"Error parsing metadata for {file_path}: {e}")
            
        # Clean up tags
        return list(set([t.strip() for t in tags if t.strip()]))

if __name__ == "__main__":
    # Test block
    import sys
    if len(sys.argv) > 1:
        print(f"Tags: {XMPParser.extract_tags(sys.argv[1])}")

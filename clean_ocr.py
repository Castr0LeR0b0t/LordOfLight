def clean_ocr_file(input_file, output_file):
    try:
        # Read the file as binary and remove null bytes
        with open(input_file, 'rb') as f:
            content = f.read()
        
        # Remove null bytes and decode to string
        cleaned_content = content.replace(b'\x00', b'').decode('utf-8', errors='ignore')
        
        # Write cleaned content to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
            
        print(f"Successfully cleaned file. Output saved to: {output_file}")
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    input_file = 'ocr_zelazny_-_lord_of_light.txt'
    output_file = 'cleaned_lord_of_light.txt'
    clean_ocr_file(input_file, output_file)

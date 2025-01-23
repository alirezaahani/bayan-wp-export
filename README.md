# Blog.ir to WXR Exporter

This script exports posts, comments, tags, and categories from a blog on `blog.ir` to a WXR (WordPress eXtended RSS) file. The WXR file can then be imported into a WordPress site.

## Requirements

- Python 3.x
- `lxml` library
- `requests` library
- `beautifulsoup4` library
- `jdatetime` library

You can install the required libraries using pip:

```sh
pip install lxml requests beautifulsoup4 jdatetime
```

## Usage

1. **Edit the Blog Address**

   Open the `main.py` file and replace the `BLOG` variable with your blog address:

   ```python
   BLOG = 'your_blog_address'
   ```

2. **Export Cookies**

   Export your cookies from your browser and save them into a file named `cookies.txt` in the same directory as `main.py`. The cookies file should be in the Netscape format.

3. **Run the Script**

   Run the script to generate the WXR file:

   ```sh
   python main.py
   ```

   The script will create an `export.xml` file containing your blog's data in the WXR format.

## Notes

- The script currently fetches the first 100 posts and comments. You may need to modify the script to handle pagination if you have more posts or comments.
- The script uses the `jdatetime` library to handle Persian dates and convert them to Gregorian dates.

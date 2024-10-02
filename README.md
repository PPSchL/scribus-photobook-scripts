### Introduction
This repository cointains a collection of scribus scripts that facilitate the creation of photobooks in scribus. You start with a page of same-size image frames that you can then adapt to your taste and needs by combinig several frames into a single one (combine images), or split a frame into several smaller ones (split image).

I started this collection of scripts because I became frustrated with the photobook printing services that do not allow saving your creations except on the site itsself. This obviously means that if the site closes down or for whatever reasons decides to remove your photobooks, you will have to start from scratch. After some research on alternatives, I decided to create my photobooks in scribus and export them to pdf for screen viewing (at 150 ppi) or printing (at 300 ppi). Your scribus photobooks are best saved with your images, are very small because they do not contain the pictures themselves but only links to the pictures, and can use all sorts of image formats, including even the new and very convenient JPEG XL files. Pdfs can be generated as needed, with different resolutions and color profiles.

As I live in France, I had some problems finding a photobook print service that accepts pdf files. I finally found [flexilivres](https://www.flexilivre.com/fichier/), which gives me good results (I am not linked to them in any way, and do not endorse them, I just provide this information for your convenience). I found that they apparently convert PDF pages to image files, so you may be able to manually use a similar approach to use other print services with pdf files.

These photobook scripts are very simple and tailored to my specific way of working, therefore I do not accept collaboration on improving the scripts. You are obviously wellcome to fork or clone the repository, although if you are fluent in python programming you definitely do not need my scripts!
### installation
- download all files from github resulting in a zip file (click on the **<>Code** menu and select **Download Zip**):
  
  ![down-load menu](docs/img/download-zip.png)
  
- create a directory for scribus scripts at a convenient location
- define this directory as scripts directory in scribus preferences
- extract all files (including hidden directories and files) into this scripts directory
- make sure all the scripts have execution privilege (depending on your operating system)
- **CAVEAT**: the scripts have only been tested under Linux

- launch scribus and within scribus execute the setup_photobook_tkinter.py script which you should see when accessing the Scripts menu and launching a script
- if setup_photobook_tkinter.py does not work (eg Apple Mac), run setup_photobook.py
- in this setup script, the first step is to select the previously defined scripts directory, then select your preferred units and menu language
- you can redo the setup and overwrite the previous configuration as often as required...the script path will be conserved but can be changed if needed

- you can now use the different scripts

### use for photobook creation
- open the file or create the document you want to work with. **important** the scripts only work if a document is open.
- the scripts use the margins defined in your document
- **important:** the scripts will lock the positions and sizes of the created photoframes, unlock (CTRL-L) to be able to delete or change the size of any photos, relock (CTRL-L) after your modification to avoid accidentally moving the frames. You can also convert a photo frame to a text frame by the standard scribus commands (Object menu, unlock frame first!).
- the scripts create empty frames, use standard scribus commands to select photos for your frames (right click on frame, or CTRL-I to import image). Again use standard scribus commands to adapt the size of the image to the frame, etc. Scribus also has an internal script (align_image_in_frame) to adapt the image to the frame.
- I usually start with a white background, and once the page is completely finalized I swith to a black background because I like the higher contrast the darker background provides.

#### photobook-page
- creates a page of same size photo frames within the margins defined in the scribus file
- you have to enter the number of photos in width and height as well as the distance between photos
- once the page is created, you can use the other scripts like split-image or combine-images to alter the page to your taste.
- example:
  
  ![standard page](docs/img/photobook-standard.png)

#### photobook-1-image
- complement to photobook-page, but only creates 1 image at the coordinates you specify
- you still have to enter the number of photos in width and height as well as the distance between photos
- then enter coordinates relative to the number of photos in each direction eg 1,1 is top left

#### photobook-split-image
- select one photograph and execute the script
- enter the number of photos in width and height as well as the distance between photos
- the photo will be split into a group of photos  according to your choice

#### photobook-combine-images
- select a group of images/photos
- execute the script
- a single photo of the size of the group of images will be created
- all selected photo frames will be deleted (make sure to select all the frames you want to be replaced)
- if the frames already contain photos, the one selected first will be in the final, larger frame

#### swap-frames
- select two frames or photos (select first, SHIFT-click second)
- execute the script
- the content of the frames will be swapped

#### photobook-page-with-bleed
- creates a page without margins. Images/photo edges are aligned with the outer border of the bleed, ie the bleed area will be cut during printing to obtain a page without a margin at all. Make sure no important part of your photos is within the bleed.
- by default, gutter is set to 0, but this can be changed
- run the script, then enter the number of photos in width and height as well as the distance between photos
- example of a page :
- 
  ![page using bleed](docs/img/with-bleed.png)

#### photobook-page-asymmetric
- this script creates a page where the photos are not all of the same size, it is a handy way to quickly create a page with a mixture of landscape and portrait photos. Here is an example:
  
  ![standard assymetric page](docs/img/asymmetric.png)

- run the script, then enter the number of picture lines (with one photo for which you specify the image ratio, and another photo filling up the remaining space on the line)
- enter the image ratio for the first photo, eg standard 35 mm ratio=3/2 or 1.5, micro-four thirds: 4/3 or 1.33. You can enter the value as a ratio (eg 3/2), or a real number (eg 1.5). You can enter any ratio as long as the picture width does not increase beyond the page size or the complementary portrait photo does not become to oblong (ratio>2); You can also specify an image ratio<1 to obtain a portrait as the first picture, but this effect can be obtained differently (see below)
- enter the gutter (distance between images)
- enter the direction, ie left2right (default) or right2left: right2left will put the complementary picture first eg see this example:

  ![right2left](docs/img/right2left.png)

  and compare with the standard above
- enter the page type, ie either all image lines are identical (constant) or the landscape/portait and portrait/landscape page alternate (alternate). See an example for alternate here: 
  
  ![alternate](docs/img/alternate.png)

### use for photodiary creation

- in this context, a photodiary is a photobook containg one or several photos per day, with an accompanying text
- the top of the page states the month
- on the left or right of the photos for each day, the day in the month is indicated
- these scripts are specifically written for 3 days per page, but the acta-1-group allows to adapt the page for showing 2 or three days
- these scripts use a "base" definition of what a generic "day" group should look like. If you change anything (eg color,font) in this "base" file it will change in the resulting photobook from that change point onwards. This is a convenient way to change the look of the resulting photodiary. This file is located in the .photobook hidden directory within the script directory and is called "Annales_base.sla". It is a standard scribus file. You may have to change your operating system preferences to see the hidden directory (under gnome file manger: ctrl-h)

#### Acta-new-page
- creates a page of three photos and text frames, eg three days of diary:
  
  ![diary page](docs/img/diary-standard.png)

#### acta-1-group
- creates a group for a single day, you will have to specify where on the page it is to be created (top (1), middle (2), or bottom (3))
- you can create a standard day group, 
  - a day with central text (instead of left or right text)
- 
  ![central text](docs/img/diary-central.png)
  
  or 

  - a bigger group for more photos/day taking up the space for 2 days (double)
  
    ![eg double](docs/img/diary-double.png)
    
    or

  - three days (whole page)
   
    ![eg whole page](docs/img/diary-whole-page.png)

- play with it and the use of each option will quickly become obvious
- you can then create different types pages: eg a page with double space at the top (position 1), and simple central text at the bottom (position 3)
  
  ![diary example page](docs/img/diary-example.png)

### More advanced personalization
I have not yet added the possibility to define the default distance between images (gutter) through the setup scripts. The present values are my preferred defaults and can be changed when running the scripts. In order to change the default values, right now you will have to change the code in the setup_photobook.py file.
How-to:
- Open this file in your preferred text editor
- find the "def set_my_defaults(my_units):" line 
- below this line, you will have all the default values that you can change to your convenience
- all the distance values (bleed, gutters) are in mm, to put in your preferred values change them to mm first: eg if you want the gutter to be 0.1 inch instead of 3 mm, replace 3 by 2.54

### For those looking at the source code
- Sorry, not everything is correctly commented yet. Well, actually most functions are not commented at all (yes, I know!)
- scribus_acta, coming later, is better commented, but ok, I absolutely will comment the main module scribus_paul shortly ;-)



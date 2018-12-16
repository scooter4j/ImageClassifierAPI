// How to use:
// 1. navigate to images.google.com
// 2. search for the images you want (e.g. Japanese beetle)
// 3. open the Javascript console (Chrome: Developer Tools > Console tab)
// 4. back in the browser window, scroll down until you've seen all the images you want
//    to use for training
// 5. paste the following code into the Javascript console and "enter" to execute it. This
//    will cause the download of a file named 'urls.txt' to the Downloads folder.
// 6. that's all in this bit. Next step is to download all the images from the list of urls
//    that were just created.... to do that, execute download_images.py
//

// pull down jquery into the JavaScript console
var script = document.createElement('script');
script.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(script);

// grab the URLs
var urls = $('.rg_di .rg_meta').map(function() { return JSON.parse($(this).text()).ou; });

// write the URls to file (one per line)
var textToSave = urls.toArray().join('\n');
var hiddenElement = document.createElement('a');
hiddenElement.href = 'data:attachment/text,' + encodeURI(textToSave);
hiddenElement.target = '_blank';
hiddenElement.download = 'urls.txt';
hiddenElement.click();

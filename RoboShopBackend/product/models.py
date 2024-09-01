from django.db import models

from io import BytesIO
from PIL import Image
from froala_editor.fields import FroalaField
from froala_editor.fields import FroalaEditor
from django.core.files import File

class MyFroalaEditor(FroalaEditor):
    def trigger_froala(self, el_id, options):
        js_str = """
        <script>
        FroalaEditor.DefineIcon('insertCodeBlock', {
        NAME: 'code',
        SVG_KEY: "codeView",
        });
        FroalaEditor.RegisterCommand('insertCodeBlock', {
        title: 'Insert Code',
        icon: 'insertCodeBlock',
        focus: true,
        undo: true,
        refreshAfterCallback: true,
        callback: function () {
          // Insert the code section where the cursor is
          this.html.insert('<div class="code_area"><pre><code> </code></pre></div></br>');
          this.event.focus();
        },
      });
            new FroalaEditor('#%s', %s)
        </script>""" % (el_id, options)
        return js_str

class MyFroalaField(FroalaField):
    def __init__(self, *args, **kwargs):
        super(MyFroalaField, self).__init__(*args, **kwargs)
    
    def formField(self, **kwargs):
        if self.use_froala:
            widget = MyFroalaEditor(options = self.options, theme = self.theme, 
                                    plugins = self.plugins, image_upload = self.image_upload,
                                    file_upload = self.file_upload, third_party = self.third_party)

        defaults = {'widget':widget}
        defaults.update(kwargs)
        return super(FroalaField, self).formfield(**defaults)
    
class Category(models.Model):
    name = models.CharField(max_length=300)
    show_on_home = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(upload_to='categoryImages/', null=True, blank=True)
    def __str__(self) -> str:
        return self.name

class Sub_category(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='SubCategoryImage/',null=True,blank=True)
    def __str__(self):
        return self.name    
        
        

class Product(models.Model):
    
    op = {'options':{
    
    "toolbarButtons": [[
            "bold",
            "italic",
            "underline",
            "strikeThrough",
            "subscript",
            "superscript",
          ], [
            "fontFamily",
            "fontSize",
            "textColor",
            "backgroundColor",
            "inlineStyle",
            "paragraphStyle",
            "paragraphFormat",
            
          ],["align", "formatOL", "formatUL", "outdent", "indent",],"-",["insertLink", "insertImage", "insertVideo","insertCodeBlock"],["undo", "redo","fullscreen"],],


    "icons" : {"insertCodeBlock":"<i class=\"fa fa-code\"></i>"}
  }}
    
    
    category = models.ManyToManyField(Category, blank=True)
    sub_category = models.ManyToManyField(Sub_category, blank=True) 
    name = models.CharField(max_length=1000)
    product_code = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=7, decimal_places=2)
    after_discount = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    description = models.TextField(max_length=10000)
    ratting = models.DecimalField(max_digits=5, decimal_places=2)
    color = models.CharField(max_length=1000)
    stock = models.IntegerField()
    total_review = models.IntegerField()
    in_stock = models.BooleanField(default=False)
    buying_price = models.IntegerField(null=True,blank=True)
    product_discription = MyFroalaField(null = True, blank = True , **op)
    product_tutorial = MyFroalaField(null = True, blank = True , **op)
    
    def __str__(self):
        return self.name

class ProductMedia(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='All_Product_Additional_Photo/')

    def __str__(self) -> str:
        return self.product.name
    


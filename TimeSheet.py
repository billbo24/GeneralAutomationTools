


#%%
#Going to attempt to make a function that opens Unanet and goes to my time sheet

import SearchTools as st
import ScreenshotTool as sst


#image_path = 'C:\\Users\\wfloyd\\OneDrive - The Kleingers Group\\Documents\\GeneralAutomationTools\\UnanetTest'
image_path = '/Users/williamfloyd/Documents/PythonCode/GeneralAutomationTools/UnanetTest'

#%%
sst.take_screenshot_and_save(path=image_path)



#%%
#[Image name, double click]

images = [('UnanetIcon',True,'Unanet_ALT')
          ,('WindowsLogin',False,None)
          ,('PersonalButton',False,None)
          ,('TimeSheets',False,None)]





#st.find_image_and_click('XOut',image_path)

for imageName,doubleClick,altImage in images:
    if altImage:
        st.repeat_find_click(imageName,image_path,double_click = doubleClick,alt_image=altImage)
    else:
        st.repeat_find_click(imageName,image_path,double_click = doubleClick)

# %%

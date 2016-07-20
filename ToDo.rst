Prepare a class for every load datas
in that class toy have the spectrum, and all calculation

Generalize read/print function and try to implement only write mode (also watch
this: You are creating a write-only workbook. At the name suggests, this is 
designed for  streaming data to a workbook so some operations, such as looking
up cells do not work. To add data you should use the append() method. If you do
need to add formatting or comments to individual cells you can include a
WriteOnlyCell in the iterable that you pass into append().)

Check if file is already create, in that case do something....

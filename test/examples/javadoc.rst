
.. c:function:: int frob2(struct list *list, enum mode mode)

   Custom comment transformations.

   Documentation comments can be processed using the hawkmoth-process-docstring
   Sphinx event. You can use the built-in extensions for this, or create your
   own.

   In this example, hawkmoth.ext.javadoc built-in extension is used to support
   Javadoc-style documentation comments.


   :param list: The list to frob.

   :param mode: The frobnication mode.

   :return: 0 on success, non-zero error code on error.

   :since: v0.1


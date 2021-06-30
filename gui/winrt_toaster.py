from winrt.windows.ui.notifications import ToastNotificationManager, ToastNotification, ToastTemplateType

def toast_notification(AppID, title, text):
    XML = ToastNotificationManager.get_template_content(ToastTemplateType.TOAST_TEXT02)
    t = XML.get_elements_by_tag_name("text")
    t[0].append_child(XML.create_text_node(title))
    t[1].append_child(XML.create_text_node(text))
    try:
        notifier = ToastNotificationManager.create_toast_notifier(AppID)
        notifier.show(ToastNotification(XML))
    except:
        print("Notification Center Not Available")
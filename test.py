import win32security

file1 = r'file.txt' 
file2 = r'file2.txt'

sd1 = win32security.GetFileSecurity(file1, win32security.DACL_SECURITY_INFORMATION)
# sd2 = win32security.GetFileSecurity(file2, win32security.DACL_SECURITY_INFORMATION)

dacl1 = sd1.GetSecurityDescriptorDacl()
print(dacl1)
win32security.SetNamedSecurityInfo(file2, win32security.SE_FILE_OBJECT, 
                                   win32security.DACL_SECURITY_INFORMATION, 
                                   None, None, dacl1, None)
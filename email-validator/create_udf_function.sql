create function EmailValidator(email varchar)
    returns boolean
    language java
    imports = ('@~/PLG/email-validator-1.0-SNAPSHOT.jar')
    handler = 'com.streamsets.EmailValidator.validate'
    ;
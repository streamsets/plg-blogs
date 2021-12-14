package com.streamsets;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Email Validation UDF
 */
public class EmailValidator {

    private final String regex = "^(.+)@(.+)$";
    /**
     * @param email Email to validate.
     */
    public boolean validate(String email) {

        Pattern pattern = Pattern.compile(regex);
        Matcher  matcher = pattern.matcher(email);

        return matcher.matches();
    }
}

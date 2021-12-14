package com.streamsets;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

/**
 * Unit test for simple App.
 */
class AppTest {
    /**
     * Rigorous Test.
     */
    @Test
    void testApp() {
        EmailValidator ev = new EmailValidator();
        
        assertEquals(true, ev.validate("test@me.com"));
        assertNotEquals(true, ev.validate("test!me.com"));
    }
}

/*
 * Photon firmware
 * Assumes the relay board is wired to D0
 *
 * Commands:
 *   sprinkle on
 *   sprinkle off
 *
 */

int relay = D0;
bool relay_on = false;
long tstart = 0;
long tend = 0;

void setup() {
    pinMode(relay, OUTPUT);
    digitalWrite(relay, LOW);
    Particle.function("sprinkle", sprinkle);
}

void loop() {
    bool expired = false;
    if (relay_on) {
        int ct = millis();
        if (tstart < tend && ct > tend)
            expired = true;
        else if (ct > tend && ct < tstart)
            expired = true;
        if (expired) {
            digitalWrite(relay, LOW);
            relay_on = false;
            tstart = 0;
            tend = 0;
        }
    }
}
int sprinkle(String command) {
    int rvalue = 1;
    if (command == "on") {
        digitalWrite(relay, HIGH);
        relay_on = true;
        tstart = millis();
        tend = tstart + 1000 * 60 * 2;
    } else if (command == "off") {
        digitalWrite(relay, LOW);
        relay_on = false;
        tstart = 0;
        tend = 0;
    } else {
        rvalue = 0;
    }
    return rvalue;
}


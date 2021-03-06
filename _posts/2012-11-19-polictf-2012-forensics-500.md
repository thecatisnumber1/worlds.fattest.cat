---
title: "PoliCTF 2012: Forensics 500"
categories: ctf
layout: post
---

This problem presents [a pcap file][communication.pcap], along with the flavor text "Let's call someone from the old days".

Digging into the pcap file, we find a SIP call from `danielle@10.0.42.14` to `6599@10.0.42.1`.  Digging into the RTP conversation, we find two audio streams:

[![danielle@10.0.42.14 to 6599@10.0.42.1][danielle_6599.png]<br/>danielle@10.0.42.14 -> 6599@10.0.42.1][danielle_6599.au]

[![6599@10.0.42.1 to danielle@10.0.42.14][6599_danielle.png]<br/>6599@10.0.42.1 -> danielle@10.0.42.14][6599_danielle.au]

The second one just contains a rickroll, but the first one contains what turns out to be a [1200 baud AFSK][wikipedia_afsk] signal (which we figured out after annoying other teammates by playing all of the wikipedia audio samples for [radio modulation modes][wikipedia_modulation] and looking for one that sounded similar).

After some trial and error with various AFSK1200 decoders, we ended up successfully decoding the sample using a version of [QTMM][qtmm] that we modified to remove the "helpful" feature that converts all non-printable ASCII characters received to `'.'`.  After decoding, we got:

    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x3c\xfd\xca\x40\x00\x40\x06\x28\x97\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x3f\x7c\x00\x00\x00\x00\xa0\x02\x04\x00\xc1\x9a\x00\x00\x02\x04\x01\x00\x04\x02\x08\x0a\x04\xa7\xc2\xb6\x00\x00\x00\x00\x01\x03\x03\x07
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x3c\xfd\xcb\x40\x00\x40\x06\x28\x96\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x3f\x7c\x00\x00\x00\x00\xa0\x02\x04\x00\xc0\x6e\x00\x00\x02\x04\x01\x00\x04\x02\x08\x0a\x04\xa7\xc3\xe2\x00\x00\x00\x00\x01\x03\x03\x07
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x34\xfd\xcc\x40\x00\x40\x06\x28\x9d\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x3f\x7d\x7a\x0c\xd3\xbd\x80\x10\x00\x08\xfc\xc9\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa2\xb4
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x40\xfd\xcd\x40\x00\x40\x06\x28\x90\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x3f\x7d\x7a\x0c\xd3\xbd\xb0\x10\x00\x08\x29\xf2\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa3\xe1\x01\x01\x05\x0a\x7a\x0c\xd3\xbc\x7a\x0c\xd3\xbd
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x40\xfd\xce\x40\x00\x40\x06\x28\x8f\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x3f\x7d\x7a\x0c\xd3\xbd\xb0\x10\x00\x08\x27\xef\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa5\xe4\x01\x01\x05\x0a\x7a\x0c\xd3\xbc\x7a\x0c\xd3\xbd
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x01\x00\xfd\xcf\x40\x00\x40\x06\x27\xce\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x3f\x7d\x7a\x0c\xd3\xbd\x80\x10\x00\x08\xad\xbf\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa5\xe4\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\xaf\x00\x00\x00\xaf\x01\x03\x00\x00\x00\xb1\x5c\x1c\x36\x00\x00\x00\x06\x50\x4c\x54\x45\xff\xff\xff\x00\x00\x00\x55\xc2\xd3\x7e\x00\x00\x01\xa3\x49\x44\x41\x54\x48\x89\xbd\x97\xc1\xb1\x83\x30\x0c\x44\x37\x93\x83\x8f\x94\xe0\x4e\xa0\x31\x66\x60\x26\x8d\x41\x27\x94\xc0\x91\x03\x83\xfe\xae\xcc\xcf\xff\x0d\x2c\x3e\x38\xf0\xcc\xc1\x96\x56\x6b\x05\x78\x7e\x94\xe0\xc0\xb0\xbf\x73\xda\xca\xaa\xf7\xc5\x8b\x17\xa0\xe2\x45\xcc\xa7\x11\x65\xdd\x21\x66\xc5\x6b\x9c\x15\x3d\x49\x5c\x98\x36\x7e\x30\xc5\x13\x98\xbf\xd3\xa6\x3d\xe1\x31\x8c\x57\x9c\x88\xa5\xfb\x6c\xc7\x13\x58\xf1\xe6\xc4\xec\xde\xf8\x2f\x0d\x2e\x2c\x15\x31\xb1\x63\xbd\xa7\x7f\x62\x33\xe1\x56\x29\xab\x84\xcc\x08\xd4\x5f\x62\xc5\xc3\x2e\x21\xc7\x67\x0b\x69\x38\x9f\xdc\xb8\x67\xa8\xe3
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x01\x00\xfd\xd0\x40\x00\x40\x06\x27\xcd\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x40\x49\x7a\x0c\xd3\xbd\x80\x10\x00\x08\xf7\xac\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa5\xe4\xea\x66\x85\xa1\xc5\xbb\x1e\x66\x3c\x50\x46\xb9\x76\x80\x6b\xdc\x4e\xaa\xca\x89\x95\x62\x12\xbc\xe3\x5b\xae\x7a\x75\xe2\xf4\x23\x96\xcd\x5c\x8f\xbe\x53\xd0\xf9\x95\x36\x68\xc4\xac\x98\x19\x8c\xf2\xfb\x76\x08\x70\xcd\x8c\x35\x24\x5f\x9e\x5b\xe4\x18\x62\x86\x1b\xf7\xdd\x99\x3b\x51\xbc\x53\x50\x53\x13\xb2\x0f\xeb\xf0\x95\x42\xfe\x84\xd4\x5c\xff\xee\x1d\x23\xce\x8a\xe9\x3b\x3a\x53\xd0\x21\x0e\x95\xab\x19\x33\xca\xdc\x49\x30\xc5\xb9\xc6\x08\x8c\xd5\x8c\xef\xfb\xba\x5d\x30\xa9\x66\x8a\x0c\x56\x8c\x41\x77\x1a\xcb\x75\xe3\x53\xfa\x3e\x3d\x6a\x71\x63\x16\x69\xb4\x28\xf3\xdc\x19\x7e\x58\x71\x09\x79\x2d\xfb\x93\x9a\xa6\xc4\xc3\x67\xef\xe0\xc4\x39\x98\xe2\x29\x58\xa9\x27\xca\x85\x76\x78\x23\x2e\x92\x11\x77\x92\x96\xaf\x0f\x32\xd9\x56\x9c\x83\x35\x1b\xcd\x75\x43\x22\x33\xe3\xd6\x51\xeb\x82\x41\x5a\xa0\xee\x34\x37\x5e
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x8a\xfd\xd1\x40\x00\x40\x06\x28\x42\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x41\x15\x7a\x0c\xd3\xbd\x80\x18\x00\x08\x02\xba\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa5\xe4\xd4\x51\xd3\x75\x19\xef\x3d\x1b\xce\x69\x2b\x66\xdc\x7a\x4d\x92\x54\xb3\xf6\x95\x29\x7e\x02\x87\x24\x8d\xaf\x29\xb9\x71\x76\xb6\x32\x25\x65\x77\xac\x61\xc6\x8a\xb7\x3a\xdb\xd6\x02\x96\x8b\xfa\x4a\x9d\x19\xf1\xfd\x1f\x10\xcd\x7f\x39\xcd\xdf\x26\xde\x84\x9f\x1f\x3f\x12\x35\xc5\xcb\x56\x7f\xcb\xc1\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x34\xfd\xd2\x40\x00\x40\x06\x28\x97\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x41\x6b\x7a\x0c\xd3\xbd\x80\x11\x00\x08\xf7\xaa\x00\x00\x01\x01\x08\x0a\x04\xa7\xc4\xf6\x00\x12\xa5\xe4
    AFSK1200: fm OTA22-0 to NOCALL-0 UI  pid=CC
    \x45\x00\x00\x40\xfd\xd3\x40\x00\x40\x06\x28\x8a\x0a\x2b\x00\x01\x0a\x2b\x00\x04\x9a\xd8\x27\x0f\xa9\xfd\x41\x6c\x7a\x0c\xd3\xbd\xb0\x10\x00\x08\x25\x3a\x00\x00\x01\x01\x08\x0a\x04\xa7\xc5\x2b\x00\x12\xa6\x75\x01\x01\x05\x0a\x7a\x0c\xd3\xbc\x7a\x0c\xd3\xbd

Each packet has a 52-byte header, followed by a payload.  If you concatenate the payloads of packets 6 onwards, you find a PNG containing a QR code:

![PNG from decoded audio][danielle_6599_afsk1200_decoded.png]

Decoding this QR code yields the text `The key is: 73e4geru3i21eWuypzFIueK`, and we're done.

[communication.pcap]: /postfiles/2012-11-19-polictf-2012-forensics-500/communication.pcap
[danielle_6599.au]: /postfiles/2012-11-19-polictf-2012-forensics-500/danielle_6599.au
[danielle_6599.png]: /postfiles/2012-11-19-polictf-2012-forensics-500/danielle_6599.png
[6599_danielle.au]: /postfiles/2012-11-19-polictf-2012-forensics-500/6599_danielle.au
[6599_danielle.png]: /postfiles/2012-11-19-polictf-2012-forensics-500/6599_danielle.png
[danielle_6599_afsk1200_decoded.png]: /postfiles/2012-11-19-polictf-2012-forensics-500/danielle_6599_afsk1200_decoded.png

[wikipedia_afsk]: https://en.wikipedia.org/wiki/Frequency-shift_keying#Audio_FSK
[wikipedia_modulation]: https://en.wikipedia.org/wiki/Category:Quantized_radio_modulation_modes
[qtmm]: https://github.com/csete/qtmm

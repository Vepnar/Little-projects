<?php
// Author: Arjan de Haan (Vepnar)
// Illegal google translate api!
// Usage: translate("en","ge", "Hello World!")
// To Translate "Hello World!" to German
$_BASE_URL = 'http://translate.google.com/m?hl=%s&sl=%s&q=%s';
// Store 
$_HTTP_HEADER = array(
    'http'=>array(
      'method'=>"GET",
      'header'=>"Accept-language: en\r\n" .
                "Cookie: foo=bar\r\n" .
                "User-agent: Mozilla/4.0 (" .
                "compatible;" .
                "MSIE 6.0;" .
                "Windows NT 5.1;" .
                "SV1;" .
                ".NET CLR 1.1.4322;" .
                ".NET CLR 2.0.50727;" .
                ".NET CLR 3.0.04506.30" .
                ")\r\n"
    )
);

function _send_request($to_language, $from_language, $message) {
  global $_BASE_URL, $_HTTP_HEADER;

  // Process url
  $processed_url = sprintf($_BASE_URL, $to_language, $from_language, urlencode($message));

  // Make request
  $context = stream_context_create($_HTTP_HEADER);
  $file = file_get_contents($processed_url, false, $context);
  return $file;
}

function translate($from,$to,$message) {
    // Recieve google translate html page
    $google_html = _send_request($to,$from,$message);
    // Selected translation and return it
    preg_match('/class="t0">(.*?)</', $google_html, $translation);
    return $translation[1];
}

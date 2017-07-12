(ns todo
  (:use 
    arcadia.core 
    arcadia.linear
    hard.core))

'[repl
  ([/] history + navigation
    ([x] don't record duplicate history)
    ([ ] prevent editing above history prompt?))]

'[interface
  ([x] better socket view insertion - only create second group if none exists)
  ([ ] socket commands in context menu)
  ([ ] research best default key commands (maybe use sublimeREPL's layout))]

'[advanced
  ([ ] extend to system processes (pipes))
  ([ ] allow customizable command wrapping + namespace sniffing
    ([ ] template with tokens for entered text and regex to apply to current view?))]

'[bugs
  ]

'(map inc (range 3))

{:asdf
 [#{}]}


(import IO)
(import Int)
(import String)

(defn joe [n] (* n n))

(joe 8)

(print (ref (append "hello" (str (joe 8)))))

(def a 1)
(print &(str a))
(address a)


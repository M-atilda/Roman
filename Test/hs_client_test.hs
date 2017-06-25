{-# OPTIONS -Wall -Werror #-}
-- |　nict.hs
import Network.HTTP
import Text.ParserCombinators.Parsec
import Control.Applicative hiding ((<|>),many)
import Control.Exception

-- | 日本標準時 http://www2.nict.go.jp/aeri/sts/tsp/PubNtp/http.html
url :: String
url = "http://ntp-a1.nict.go.jp/cgi-bin/time"
-- url = "aaaa/bbbb"
-- url = "ntp-a1.nict.go.jp/cgi-bin/time"
-- url = "https://ntp-a1.nict.go.jp/cgi-bin/time"

-- | こういうフォーマットで返ってくる
-- | "Sat Aug 23 22:38:19 2014 JST\n"
-- | 曜日　月　 日　と　残り　に分ける

type TailString = String
data TimeFormat = Time String String Int TailString
                  deriving Show

-- | Parser 3種類
int' :: Parser Int
int' = do n <- many1 digit
          return $ read n

int :: Parser Int
int = read <$> (many1 digit)

remains :: Parser String
remains = many1 $ space <|> letter <|> digit <|> oneOf ":\n"

timeParser :: Parser TimeFormat
timeParser = (Time <$> (many letter <* space)) 
             <*> (many letter <* space)
             <*> (int <* space)
             <*> (remains)

-- | 文字列をパースする
parseTimeParser :: String -> Either ParseError TimeFormat
parseTimeParser = parse timeParser ""

-- | HTTPで時刻を取得する。これは例外を投げる可能性がある
getTime :: IO String
getTime = (Network.HTTP.simpleHTTP (getRequest url) >>= getResponseBody)

-- | main' 例外をまとめて受け取る
main' :: IO ()
main' = catch (do nictString <- getTime
                  case (parseTimeParser nictString) of
                      Left err_msg -> print err_msg
                      Right x  -> print x
        )
        ((\_ -> putStrLn "SomeException") :: SomeException -> IO ())

-- | main 例外を別々に受け取る
main   :: IO ()
main   = catches (do nictString <- getTime
                     case (parseTimeParser nictString) of
                        Left err_msg -> print err_msg
                        Right x  -> print x
        )
        [Handler ((\e -> putStrLn ("IOException " ++ show e)) :: IOException -> IO ()),
        Handler ((\e -> putStrLn ("SomeException " ++ show e)) :: SomeException -> IO ())]

select * from dataset$


--Xóa giá trị null hoặc bị trống trong book_title
delete 
from dataset$
where book_title is null or book_title =''

--Xóa giá trị null trong cột numpages
delete 
from dataset$
where numpages is null or numpages = 0
--Xóa giá trị null trong cột publisher
delete 
from dataset$
where publisher is null or publisher=''
--Xóa giá trị null trong cột format
delete 
from dataset$
where format is null
--Xóa giá trị null trong cột publicationTime
delete 
from dataset$
where publicationTime is null
--Loại bỏ giá trị lặp trong book_title (Remove duplicate)
WITH CTE AS
(
SELECT *,ROW_NUMBER() OVER (PARTITION BY book_title ORDER BY book_title) AS RN
FROM dataset$
)
DELETE FROM CTE WHERE RN<>1

select distinct book_title from dataset$
select * from dataset$

--Mã hóa dữ liệu language bị trống thành Unknown language
update dataset$
set language = 'Unknown language'
where language = '' or language is null
--test
select distinct category, count(category) from dataset$
group by category
--Mã hóa dữ liệu genres bị trống thành Unknown genres
update dataset$
set category = 'Unknown genres'
where category = ''
--Mã hóa awards thành 0: không có; 1: có giải
update dataset$
set awards = case	when awards is null or awards ='' then 0
					else 1
					end
select AVG(averageRating) from dataset$
--Chia cột averageRating lại thành cho từ 1 đến 5
update dataset$
set averageRating = case	when averageRating >=100 then averageRating/100
							when averageRating >=10 and averageRating <100 then averageRating/10
							else averageRating end

--Tạo cột mới xác định độ dài của sách
alter table dataset$
ADD book_length varchar(30)

Update dataset$
set book_length =case	when numpages <200 then 'Short'
						when numpages between 201 and 400 then 'Medium'
						when numpages between 401 and 800 then 'Long'
						else 'Epic' end


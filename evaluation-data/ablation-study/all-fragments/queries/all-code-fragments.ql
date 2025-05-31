import java

from Method m
where m.getQualifiedName().matches("org.apache.ignite%")
select m.getQualifiedName()